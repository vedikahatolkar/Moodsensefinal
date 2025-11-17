import React from "react";
import Home from "./pages/Home";
import ChatPage from "./pages/ChatPage";

export default function App() {
  const [page, setPage] = React.useState("home");

  return (
    <div style={{ fontFamily: "Inter, Arial, sans-serif" }}>
      <header style={{ padding: 12, background: "#111827", color: "white" }}>
        <h2 style={{ margin: 0 }}>MoodSense — Minimal Demo</h2>
        <nav style={{ marginTop: 8 }}>
          <button onClick={() => setPage("home")} style={{ marginRight: 8 }}>Home</button>
          <button onClick={() => setPage("chat")}>Chat / Avatar</button>
        </nav>
      </header>

      <main style={{ padding: 20 }}>
        {page === "home" && <Home onGoToChat={() => setPage("chat")} />}
        {page === "chat" && <ChatPage />}
      </main>
    </div>
  );
}
