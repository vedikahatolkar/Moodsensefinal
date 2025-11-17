import React, { useState } from "react";
import { predictText } from "../api";

export default function Home({ onGoToChat }) {
  const [text, setText] = useState("");
  const [res, setRes] = useState(null);

  async function submitText(e) {
    e.preventDefault();
    try {
      const json = await predictText(text);
      setRes(json);
    } catch (err) {
      console.error(err);
      alert("Text prediction failed");
    }
  }

  return (
    <div>
      <h3>Home — quick text test</h3>
      <form onSubmit={submitText}>
        <textarea value={text} onChange={(e) => setText(e.target.value)} rows={4} style={{ width: "100%" }} />
        <button type="submit">Analyze Text</button>
      </form>

      {res && (
        <div style={{ marginTop: 12 }}>
          <b>Mood:</b> {res.mood} <br />
          <b>Confidence:</b> {res.confidence ?? "n/a"} <br />
          <b>Response:</b> {res.reply ?? ""}
        </div>
      )}

      <div style={{ marginTop: 18 }}>
        <button onClick={onGoToChat}>Go to Chat / Avatar</button>
      </div>
    </div>
  );
}
