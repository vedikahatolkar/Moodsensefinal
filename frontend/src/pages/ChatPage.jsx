import React, { useState } from "react";
import ChatAvatar from "../components/ChatAvatar";
import AudioRecorder from "../components/AudioRecorder";

export default function ChatPage() {
  const [mood, setMood] = useState("neutral");
  const [lastResult, setLastResult] = useState(null);

  function handleResult(json) {
    // backend should return { mood: "happy", confidence: 0.92, reply: "..."}
    const detected = json?.mood || "neutral";
    setMood(detected);
    setLastResult(json);
  }

  return (
    <div>
      <h3>Chat / Avatar</h3>
      <div style={{ display: "flex", gap: 20 }}>
        <div style={{ flex: "1 1 400px" }}>
          <AudioRecorder onResult={handleResult} />
          <div style={{ marginTop: 12 }}>
            <b>Detected mood:</b> {mood}
          </div>

          {lastResult && (
            <div style={{ marginTop: 12 }}>
              <b>Reply:</b> {lastResult.reply}
            </div>
          )}
        </div>

        <div style={{ width: 600 }}>
          <ChatAvatar modelUrl="/models/woody.glb" mood={mood} />
        </div>
      </div>
    </div>
  );
}
