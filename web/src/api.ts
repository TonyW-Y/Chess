export const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export type BoardState = {
  board: string[][];
  turn: "w" | "b";
  history_len: number;
  has_moved: Record<string, number>;
  game_status: {
    status: "in_progress" | "checkmate" | "stalemate";
    winner: "w" | "b" | null;
  };
};

export type PromotionPiece = "Q" | "R" | "B" | "N";

async function handle(res: Response) {
  if (!res.ok) {
    const txt = await res.text().catch(() => "");
    throw new Error(`HTTP ${res.status}: ${txt || res.statusText}`);
  }
  return res.json();
}

export async function getState(): Promise<BoardState> {
  const res = await fetch(`${API_BASE}/state`, {method:"GET"});
  return handle(res);
}

export async function getLegal(row: number, col: number): Promise<[number, number][]> {
  const res = await fetch(`${API_BASE}/legal`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({row, col})
  });
  if (!res.ok) { return []; }
  const data = await res.json();
  return data.legal_moves || data.moves || [];
}

export async function makeMove(
  from_row: number, from_col: number, to_row: number, to_col: number, promotion?: PromotionPiece
) {
  const res = await fetch(`${API_BASE}/move`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({from_row, from_col, to_row, to_col, promotion})
  });
  return handle(res);
}

export async function undo() {
  const res = await fetch(`${API_BASE}/undo`, {method:"POST"});
  return handle(res);
}

export async function reset() {
  const res = await fetch(`${API_BASE}/reset`, {method:"POST"});
  return handle(res);
}
