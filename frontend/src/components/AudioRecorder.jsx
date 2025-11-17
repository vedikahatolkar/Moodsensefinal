import React, { useRef, useState } from "react";
import { predictSpeech } from "../api";

export default function AudioRecorder({ onResult }) {
  const mediaRef = useRef(null);
  const [rec, setRec] = useState(false);

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mr = new MediaRecorder(stream);
    const data = [];
    mr.ondataavailable = (e) => data.push(e.data);
    mr.onstop = async () => {
      const blob = new Blob(data, { type: "audio/webm" });
      try {
        const json = await predictSpeech(blob);
        onResult(json);
      } catch (err) {
        console.error(err);
        alert("Speech prediction failed");
      }
    };
    mediaRef.current = mr;
    mr.start();
    setRec(true);
  }

  function stopRecording() {
    const mr = mediaRef.current;
    if (mr && mr.state !== "inactive") {
      mr.stop();
    }
    setRec(false);
  }

  return (
    <div>
      <button onClick={startRecording} disabled={rec}>Start</button>
      <button onClick={stopRecording} disabled={!rec}>Stop</button>
    </div>
  );
}
