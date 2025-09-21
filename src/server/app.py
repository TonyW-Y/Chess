import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
from typing import List, Tuple, Optional
import time
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

# Import after environment check to support hot reload in development
if os.getenv("ENV") != "development":
    from src.engine.chess_board import Chess_Board
    from src.engine.engine import Engine
else:
    # This allows hot reloading in development
    import importlib
    from importlib import util
    
    def dynamic_import(module_path, class_name):
        spec = importlib.util.find_spec(module_path)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    
    Chess_Board = dynamic_import("src.engine.chess_board", "Chess_Board")
    Engine = dynamic_import("src.engine.engine", "Engine")

# Environment configuration
ENV = os.getenv("ENV", "production")
IS_PRODUCTION = ENV == "production"
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "https://chess-frontend-fz6z.onrender.com",  # Production frontend
    "https://chess-backend-fr4r.onrender.com"   # Backend URL for reference
]

# Application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize resources
    app.state.start_time = time.time()
    
    # Initialize game state
    app.state.board = Chess_Board()
    app.state.engine = Engine(app.state.board)
    
    yield
    
    # Cleanup on shutdown
    # Add any cleanup code here if needed

app = FastAPI(
    title="Chess Engine API",
    description="A REST API for the Chess Engine",
    version="1.0.0",
    docs_url="/docs" if not IS_PRODUCTION else None,  # Disable in production
    redoc_url=None,  # Disable ReDoc in production
    lifespan=lifespan
)

# Middleware order matters. Add redirect and other middleware first, then CORS LAST
# so that CORS headers are added even on redirects and errors.

# Security headers middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # In production, replace with your domain
)

# GZip compression for responses
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Force HTTPS in production (added before CORS so CORS can wrap it)
if IS_PRODUCTION:
    app.add_middleware(HTTPSRedirectMiddleware)

# CORS middleware (add last)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https?://([a-zA-Z0-9-]+\.)*onrender\.com",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Length", "X-Request-ID"],
    max_age=600,  # Cache preflight request for 10 minutes
)

# Static files configuration
if IS_PRODUCTION:
    # In production, serve from the correct path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    assets_path = os.path.join(project_root, "assets")
    
    # Ensure assets directory exists
    if not os.path.exists(assets_path):
        os.makedirs(assets_path, exist_ok=True)
    
    # Mount static files
    app.mount(
        "/assets",
        StaticFiles(directory=assets_path, check_dir=True),
        name="assets"
    )
else:
    # In development, use the local assets
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    assets_path = os.path.join(project_root, "assets")
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

# Game state is now managed in the lifespan event

class MoveBody(BaseModel):
    from_row: int
    from_col: int
    to_row: int
    to_col: int
    promotion: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "from_row": 6,
                "from_col": 4,
                "to_row": 4,
                "to_col": 4,
                "promotion": None
            }
        }

class CoordBody(BaseModel):
    row: int
    col: int
    
    class Config:
        schema_extra = {
            "example": {
                "row": 1,
                "col": 0
            }
        }

@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers and monitoring"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "uptime": time.time() - app.state.start_time,
        "environment": ENV
    }

@app.get("/state")
async def get_state():
    """Get the current game state"""
    board = app.state.board
    engine = app.state.engine
    
    status, winner = engine.get_game_status()
    return {
        "board": board.board,
        "turn": board.color,
        "history_len": len(board.history),
        "has_moved": board.has_moved,
        "game_status": {
            "status": status,
            "winner": winner,
        }
    }

@app.post("/reset")
async def reset():
    """Reset the game to the initial state"""
    app.state.board.reset_board()
    app.state.engine.reset()
    return await get_state()

@app.post("/undo")
async def undo():
    """Undo the last move"""
    if not app.state.engine.undo_move():
        raise HTTPException(
            status_code=400,
            detail={"error": "No moves to undo", "code": "no_moves_to_undo"}
        )
    return await get_state()

@app.post("/legal")
async def legal(coord: CoordBody):
    """Get legal moves for a piece at the given coordinates"""
    if not (0 <= coord.row < 8 and 0 <= coord.col < 8):
        raise HTTPException(
            status_code=400,
            detail={"error": "Invalid coordinates", "code": "invalid_coordinates"}
        )
    return {
        "legal_moves": app.state.engine.legality.get_legal_moves(coord.row, coord.col)
    }

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
        "game_status": {
            "status": status,
            "winner": winner,
        }
    }

# Root endpoint for API documentation and health
@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint that provides API information"""
    return {
        "message": "Chess Engine API",
        "status": "operational",
        "environment": ENV,
        "documentation": "/docs" if not IS_PRODUCTION else "Disabled in production",
        "uptime": time.time() - app.state.start_time,
        "version": "1.0.0"
    }

# Custom exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, dict) else str(exc.detail),
            "code": getattr(exc, "code", "unknown_error"),
            "path": request.url.path
        }
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"error": "Resource not found", "code": "not_found"}
    )

@app.exception_handler(500)
async def server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "code": "internal_error"}
    )
