import { useEffect, useState } from 'react'
import { BoardState, PromotionPiece, getState, makeMove, undo, reset } from './api'
import Board from './Board'

export default function App() {
  const [state, setState] = useState<BoardState | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const load = async () => {
    setLoading(true)
    try {
      const s = await getState()
      setState(s)
    } catch (e: any) {
      setError(e.message || 'Failed to load state')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const onMove = async (from: [number, number], to: [number, number], promotion?: PromotionPiece) => {
    try {
      const res = await makeMove(from[0], from[1], to[0], to[1], promotion)
      // Update the state with the complete response from the server
      setState((prev: BoardState | null) => (prev ? { 
        ...prev, 
        board: res.board, 
        turn: res.turn, 
        history_len: prev.history_len + 1,
        game_status: res.game_status  // Make sure to include the updated game status
      } : prev))
      setError(null)
    } catch (e: any) {
      setError(e.message)
    }
  }

  const onUndo = async () => {
    try {
      const newState = await undo();
      setState(newState);
      setError(null);
    } catch (e: any) {
      setError(e.message);
    }
  }

  const onReset = async () => {
    try {
      const newState = await reset();
      setState(newState);
      setError(null);
    } catch (e: any) {
      setError(e.message);
    }
  }

  if (loading || !state) return <div className="container"><h2>Loading...</h2></div>

  const isGameOver = state.game_status.status !== 'in_progress';
  const winner = state.game_status.winner === 'w' ? 'White' : 'Black';

  return (
    <div className="container">
      <header>
        <h1>Chess</h1>
        {!isGameOver && (
          <div className="controls">
            <button onClick={onUndo} disabled={!state.history_len}>Undo</button>
            <button onClick={onReset}>Reset</button>
          </div>
        )}
      </header>
      
      {isGameOver ? (
        <div className="game-over">
          <h2>{state.game_status.status === 'checkmate' ? `Checkmate! ${winner} wins! 🎉` : 'Stalemate! 🏁'}</h2>
          <button className="play-again" onClick={onReset}>Play Again</button>
        </div>
      ) : (
        <>
          <div className="status">Turn: {state.turn === 'w' ? 'White' : 'Black'}</div>
          <Board board={state.board} turn={state.turn} onMove={onMove} />
        </>
      )}
      
      {error && <div className="error">{error}</div>}
    </div>
  )
}
