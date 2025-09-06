import React, { useState } from "react";
import Calculator from "./components/Calculator";
import ResultCard from "./components/ResultCard";

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  async function handleCalculate(name1, name2) {
    setLoading(true);
    setErrorMsg("");
    setResult(null);
    try {
      const resp = await fetch("/api/calculate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name1, name2 })
      });
      if (!resp.ok) {
        const j = await resp.json().catch(()=>({error:"Bad response"}));
        throw new Error(j.message || j.error || "Request failed");
      }
      const data = await resp.json();
      setResult(data);
    } catch (err) {
      setErrorMsg(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header>
        <h1>💖 Kamzy's FLAMES Love Calculator</h1>
        <p className="subtitle">Your custom FLAMES formula — remove common letters, count leftovers, circular elimination.</p>
      </header>

      <main>
        <Calculator onCalculate={handleCalculate} loading={loading} />
        {errorMsg && <div className="error">{errorMsg}</div>}
        {result && <ResultCard result={result} />}
      </main>

      <footer>
        <small>Built for Kamzy — F L A M E S (Friend, Love, Admire, Marriage, Enemy, Secret Lover)</small>
      </footer>
    </div>
  );
}

export default App;
