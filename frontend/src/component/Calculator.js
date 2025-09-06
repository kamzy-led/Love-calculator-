import React, { useState } from "react";

export default function Calculator({ onCalculate, loading }) {
  const [name1, setName1] = useState("");
  const [name2, setName2] = useState("");

  const submit = (e) => {
    e.preventDefault();
    if (!name1.trim() || !name2.trim()) return;
    onCalculate(name1.trim(), name2.trim());
  };

  return (
    <form className="calc" onSubmit={submit}>
      <input
        placeholder="Your name (e.g., Kamzy)"
        value={name1}
        onChange={(e) => setName1(e.target.value)}
      />
      <input
        placeholder="Their name (e.g., Kamo)"
        value={name2}
        onChange={(e) => setName2(e.target.value)}
      />
      <button type="submit" disabled={loading}>
        {loading ? "Calculating..." : "Calculate 💘"}
      </button>
    </form>
  );
    }
