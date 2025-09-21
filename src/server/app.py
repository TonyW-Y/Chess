import os
import time
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# ----- Environment -----
ENV = os.getenv("ENV", "development")  # Default to development for local
IS_PRODUCTION = ENV == "production"
print(f"Running in {'PRODUCTION' if IS_PRODUCTION else 'DEVELOPMENT'} mode")

# Exact frontend origin (Render)
FRONTEND_ORIGIN = "https://chess-frontend-fz6z.onrender.com"

# Allow localhost in dev; production stays locked to your Render frontend
ALLOWED_ORIGINS = [FRONTEND_ORIGIN] if IS_PRODUCTION else [
  "http://localhost:5173",
  "http://127.0.0.1:5173",
  "http://localhost:8000",
  FRONTEND_ORIGIN
]

# ----- Hot-reload friendly imports -----
if os.getenv("ENV") != "development":
    from src.engine.chess_board import Chess_Board
    from src.engine.engine import Engine
else:
    import importlib
    from importlib import util

    def dynamic_import(module_path, class_name):
        spec = importlib.util.find_spec(module_path)  # noqa: F841  # keep for dev diagnostics
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    Chess_Board = dynamic_import("src.engine.chess_board", "Chess_Board")
    Engine = dynamic_import("src.engine.engine", "Engine")

# ----- Lifespan -----
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.start_time = time.time()
    app.state.board = Chess_Board()
    app.state.engine = Engine(app.state.board)
    yield
    # cleanup here if needed

app = FastAPI(
    title="Chess Engine API",
    description="A REST API for the Chess Engine",
    version="1.0.0",
    docs_url=None if IS_PRODUCTION else "/docs",
    redoc_url=None,
    lifespan=lifespan
)

# ----- Middleware (order matters: add CORS last) -----
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])  # tighten later if desired
app.add_middleware(GZipMiddleware, minimum_size=1000)

# IMPORTANT: Do NOT force HTTPS here on Render; the platform handles TLS.
# For reference, we intentionally DO NOT add HTTPSRedirectMiddleware.

# CORS LAST so it wraps everything (Starlette applies in reverse order)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Length", "X-Request-ID"],
    max_age=600
)

# ----- Static files (optional) -----
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
assets_path = os.path.join(project_root, "assets")
if not os.path.exists(assets_path):
    os.makedirs(assets_path, exist_ok=True)
app.mount("/assets", StaticFiles(directory=assets_path, check_dir=True), name="assets")

# ----- Models -----
class MoveBody(BaseModel):
    from_row: int
    from_col: int
    to_row: int
    to_col: int
    promotion: Optional[str] = None

    class Config:
        json_schema_extra = {"example": {"from_row":6,"from_col":4,"to_row":4,"to_col":4,"promotion":None}}

class CoordBody(BaseModel):
    row: int
    col: int
    class Config:
        json_schema_extra = {"example": {"row":1,"col":0}}

# ----- Routes -----
@app.get("/health")
async def health_check():
    return {"status":"healthy","timestamp":time.time(),"uptime":time.time()-app.state.start_time,"environment":ENV}

@app.get("/state")
async def get_state():
    board = app.state.board
    engine = app.state.engine
    status, winner = engine.get_game_status()
    return {
        "board": board.board,
        "turn": board.color,
        "history_len": len(board.history),
        "has_moved": board.has_moved,
        "game_status": {"status": status, "winner": winner}
    }

@app.post("/reset")
async def reset():
    app.state.board.reset_board()
    app.state.engine.reset()
    return await get_state()

@app.post("/undo")
async def undo():
    try:
        app.state.engine.undo()
        return await get_state()
    except IndexError:
        raise HTTPException(status_code=400, detail={"error":"No moves to undo","code":"no_moves_to_undo"})

@app.post("/legal")
async def legal(coord: CoordBody):
    if not (0 <= coord.row < 8 and 0 <= coord.col < 8):
        raise HTTPException(status_code=400, detail={"error":"Invalid coordinates","code":"invalid_coordinates"})
    return {"legal_moves": app.state.engine.legality.get_legal_moves(coord.row, coord.col)}

@app.post("/move")
async def move(mv: MoveBody):
    if not (0 <= mv.from_row < 8 and 0 <= mv.from_col < 8 and 0 <= mv.to_row < 8 and 0 <= mv.to_col < 8):
        raise HTTPException(status_code=400, detail="Out of bounds")
    promotion = None
    if mv.promotion:
        p = mv.promotion.upper()
        if p not in {"Q","R","B","N"}:
            raise HTTPException(status_code=400, detail="Invalid promotion piece")
        promotion = p
    success, msg = app.state.engine.play_turn(mv.from_row, mv.from_col, mv.to_row, mv.to_col, promotion)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    status, winner = app.state.engine.get_game_status()
    return {
        "ok": True,
        "message": msg,
        "board": app.state.board.board,
        "turn": app.state.board.color,
        "game_status": {"status": status, "winner": winner}
    }

@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Chess Engine API",
        "status": "operational",
        "environment": ENV,
        "documentation": "/docs" if not IS_PRODUCTION else "Disabled in production",
        "uptime": time.time() - app.state.start_time,
        "version": "1.0.0"
    }

# ----- Exception handlers -----
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail if isinstance(exc.detail, dict) else str(exc.detail),
                 "code": getattr(exc, "code", "unknown_error"), "path": request.url.path}
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=404, content={"error":"Resource not found","code":"not_found"})

@app.exception_handler(500)
async def server_error_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error":"Internal server error","code":"internal_error"})
