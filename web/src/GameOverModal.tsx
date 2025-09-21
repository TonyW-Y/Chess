import React from 'react';

type Props = {
  status: 'checkmate' | 'stalemate';
  winner: 'w' | 'b' | null;
  onPlayAgain: () => void;
};

export default function GameOverModal({ status, winner, onPlayAgain }: Props) {
  const winnerText = winner === 'w' ? 'White' : 'Black';
  let message;
  if (status === 'checkmate') {
    message = `Checkmate! ${winnerText} wins! 🎉`;
  } else {
    message = 'Stalemate! It\'s a draw.';
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>{message}</h2>
        <button onClick={onPlayAgain}>Play Again</button>
      </div>
    </div>
  );
}
