import React from "react";

export default function ResultCard({ result }) {
  const messages = {
    F: "You two will be solid friends. Trust builds everything.",
    L: "Love is glowing — nurture it with small gestures.",
    A: "Admiration is here — a compliment might spark more.",
    M: "Marriage vibes — think long-term and meaningful promises.",
    E: "There is friction — approach gently and communicate.",
    S: "Secret lover — feelings are private. Consider careful steps."
  };

  return (
    <div className="result-card" role="status" aria-live="polite">
      <div className="emoji">{result.emoji}</div>
      <h2>{result.meaning}</h2>
      <p className="count">Leftover letters count: {result.count}</p>
      <p className="message">{messages[result.key] || result.advice}</p>
      <div className="advice">💡 {result.advice}</div>
    </div>
  );
  }
