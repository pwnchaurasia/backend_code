import { useEffect, useState } from "react";
import "./App.css";

const UI_VERSION = import.meta.env.VITE_APP_VERSION ?? "dev";

export default function App() {
  const [notes, setNotes] = useState([]);
  const [text, setText] = useState("");
  const [apiVersion, setApiVersion] = useState("…");
  const [error, setError] = useState("");

  async function load() {
    try {
      const [health, list] = await Promise.all([fetch("/api/health"), fetch("/api/notes")]);
      if (!health.ok || !list.ok) throw new Error(`API error ${health.status}/${list.status}`);
      setApiVersion((await health.json()).version);
      setNotes(await list.json());
      setError("");
    } catch (e) {
      setError(e.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function addNote(e) {
    e.preventDefault();
    if (!text.trim()) return;
    const r = await fetch("/api/notes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!r.ok) {
      setError(`Could not save note (${r.status})`);
      return;
    }
    setText("");
    load();
  }

  return (
    <main className="container">
      <h1>Notes</h1>
      <p className="versions">
        UI <code>{UI_VERSION}</code> · API <code>{apiVersion}</code>
      </p>

      <form onSubmit={addNote}>
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          maxLength={500}
          placeholder="Write a note…"
        />
        <button type="submit">Add</button>
      </form>

      {error && <p className="error">{error}</p>}

      <ul>
        {notes.map((n) => (
          <li key={n.id}>
            {n.text} <small>{new Date(n.created_at).toLocaleString()}</small>
          </li>
        ))}
      </ul>
    </main>
  );
}