from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Tuple

from src.engine.chess_board import Chess_Board
from src.engine.engine import Engine

app = FastAPI(title="Chess Engine API")

# CORS for local dev (Vite default is 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
assets_path = os.path.join(project_root, "assets")

# Serve existing piece assets so the frontend can load them
app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

# Single in-memory game instance
board = Chess_Board()
engine = Engine(board)

class MoveBody(BaseModel):
    from_row: int
    from_col: int
    to_row: int
    to_col: int
    promotion: str | None = None

class CoordBody(BaseModel):
    row: int
    col: int

@app.get("/state")
def get_state():
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
def reset():
    global board, engine
    board = Chess_Board()
    engine = Engine(board)
    return {"ok": True}

@app.post("/undo")
def undo():
    board.undo_move()
    return {"ok": True}

@app.post("/legal")
def legal(coord: CoordBody):
    piece = board.board[coord.row][coord.col]
    if piece == "--":
        return {"moves": []}
    if piece[0] != board.color:
        return {"moves": []}
    moves = engine.legality.filter_move(coord.row, coord.col)
    return {"moves": moves}

@app.post("/move")
def move(mv: MoveBody):
    if not (0 <= mv.from_row < 8 and 0 <= mv.from_col < 8 and 0 <= mv.to_row < 8 and 0 <= mv.to_col < 8):
        raise HTTPException(status_code=400, detail="Out of bounds")
    promotion = None
    if mv.promotion:
        p = mv.promotion.upper()
        if p not in {"Q","R","B","N"}:
            raise HTTPException(status_code=400, detail="Invalid promotion piece")
        promotion = p
    success, msg = engine.play_turn(mv.from_row, mv.from_col, mv.to_row, mv.to_col, promotion)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
        
    status, winner = engine.get_game_status()
    return {
        "ok": True,
        "message": msg,
        "board": board.board,
        "turn": board.color,
        "game_status": {
            "status": status,
            "winner": winner,
        }
    }

# Health
@app.get("/")
def root():
    return {"status": "ok"}
