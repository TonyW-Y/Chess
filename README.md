# Chess Engine + FastAPI + React

This project contains a Python chess engine, a FastAPI backend to expose it over HTTP, and a React (Vite) frontend.

## Run backend (FastAPI)

Prereqs: Python 3.10+

```bash
pip install -r requirements.txt
uvicorn src.server.app:app --reload --port 8000
```

The API will be available at http://localhost:8000. Piece image assets are served from `/assets`.

## Run frontend (React + Vite)

Prereqs: Node 18+

```bash
cd web
npm install
npm run dev
```

Open the frontend at http://localhost:5173.

The frontend expects the backend at http://localhost:8000.

## API Endpoints

- GET `/state` — current board (8x8), turn, history length, has_moved map
- POST `/legal` — body `{ row, col }` returns `{ moves: [[r,c], ...] }`
- POST `/move` — body `{ from_row, from_col, to_row, to_col }` makes a move
- POST `/undo` — undo last move
- POST `/reset` — reset game

## Notes

- Castling now blocks passing through check, using proper attack detection in `src/engine/legality.py`.
- Pawn promotion is auto-queen in `src/engine/make_unmake.py`.
- Pawn two-square advance requires clear intermediate square.
- Engine imports are package-safe under `src/`.
