import { useEffect, useMemo, useState } from 'react'
import { API_BASE, getLegal, PromotionPiece } from './api'

type Props = {
  board: string[][]
  turn: 'w' | 'b'
  onMove: (from: [number, number], to: [number, number], promotion?: PromotionPiece) => Promise<void> | void
}

const pieceImg = (code: string) => `${API_BASE}/assets/${code}.png`

export default function Board({ board, turn, onMove }: Props) {
  const [selected, setSelected] = useState<[number, number] | null>(null)
  const [legal, setLegal] = useState<[number, number][]>([])

  useEffect(() => {
    // clear selection on turn change
    setSelected(null)
    setLegal([])
  }, [turn])

  const onSquareClick = async (row: number, col: number) => {
    const code = board[row][col]
    if (selected) {
      // attempt move if clicked square is legal
      if (legal.some(([r, c]) => r === row && c === col)) {
        // check if promotion is needed
        let promotion: PromotionPiece | undefined
        const [sr, sc] = selected
        const moving = board[sr][sc]
        if (moving === 'wP' && row === 0) {
          const choice = (window.prompt('Promote to (Q/R/B/N):', 'Q') || 'Q').toUpperCase()
          if (['Q','R','B','N'].includes(choice)) promotion = choice as PromotionPiece
        } else if (moving === 'bP' && row === 7) {
          const choice = (window.prompt('Promote to (Q/R/B/N):', 'Q') || 'Q').toUpperCase()
          if (['Q','R','B','N'].includes(choice)) promotion = choice as PromotionPiece
        }
        await onMove(selected, [row, col], promotion)
        setSelected(null)
        setLegal([])
        return
      }
      // if clicked another own piece, update selection
      if (code !== '--' && code[0] === turn) {
        setSelected([row, col])
        const moves = await getLegal(row, col)
        setLegal(moves)
        return
      }
      // otherwise clear
      setSelected(null)
      setLegal([])
      return
    }
    // no selection yet
    if (code !== '--' && code[0] === turn) {
      setSelected([row, col])
      const moves = await getLegal(row, col)
      setLegal(moves)
    }
  }

  const boardSize = 560
  const squareSize = boardSize / 8

  const rows = useMemo<number[]>(() => Array.from({ length: 8 }, (_, r) => r), [])
  const cols: number[] = rows

  return (
    <div className="board" style={{ width: boardSize, height: boardSize }}>
      {rows.map((r: number) => (
        <div key={r} className="row">
          {cols.map((c: number) => {
            const light = (r + c) % 2 === 0
            const code = board[r][c]
            const isSelected = selected && selected[0] === r && selected[1] === c
            const isLegal = legal.some(([lr, lc]: [number, number]) => lr === r && lc === c)
            return (
              <div
                key={c}
                className={`square ${light ? 'light' : 'dark'} ${isSelected ? 'selected' : ''} ${isLegal ? 'legal' : ''}`}
                style={{ width: squareSize, height: squareSize }}
                onClick={() => onSquareClick(r, c)}
              >
                {code !== '--' && (
                  <img src={pieceImg(code)} alt={code} draggable={false} />
                )}
              </div>
            )
          })}
        </div>
      ))}
    </div>
  )
}
