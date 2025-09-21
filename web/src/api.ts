export const API_BASE = import.meta.env.VITE_API_BASE||'http://localhost:8000';

export type BoardState = {
  board: string[][];
  turn: 'w'|'b';
  history_len: number;
  has_moved: Record<string, number>;
  game_status: {status:'in_progress'|'checkmate'|'stalemate'; winner:'w'|'b'|null};
};

export type PromotionPiece = 'Q'|'R'|'B'|'N';

const parseErr = async (res:Response) => {
  try{
    const body = await res.json();
    // FastAPI handler returns {"error":<string|object>, "code": "..."}
    if(typeof body?.error==='string'){return body.error;}
    if(body?.error?.error){return body.error.error;}
    if(body?.detail){return body.detail;}
    return JSON.stringify(body);
  }catch{return res.statusText||'Request failed';}
};

const j = async (res:Response) => {
  if(!res.ok){throw new Error(await parseErr(res));}
  return res.json();
};

export async function getState():Promise<BoardState>{
  const res = await fetch(`${API_BASE}/state`, {method:'GET', cache:'no-store'});
  return j(res);
}

export async function getLegal(row:number, col:number):Promise<[number, number][]>{
  const res = await fetch(`${API_BASE}/legal`, {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    cache:'no-store',
    body:JSON.stringify({row, col})
  });
  if(!res.ok){return [];}
  const data = await res.json();
  return data.legal_moves||data.moves||[];
}

export async function makeMove(from_row:number, from_col:number, to_row:number, to_col:number, promotion?:PromotionPiece){
  const res = await fetch(`${API_BASE}/move`, {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    cache:'no-store',
    body:JSON.stringify({from_row, from_col, to_row, to_col, promotion})
  });
  return j(res);
}

export async function undo():Promise<BoardState>{
  const res = await fetch(`${API_BASE}/undo`, {method:'POST', cache:'no-store'});
  return j(res);
}

export async function reset():Promise<BoardState>{
  const res = await fetch(`${API_BASE}/reset`, {method:'POST', cache:'no-store'});
  return j(res);
}
