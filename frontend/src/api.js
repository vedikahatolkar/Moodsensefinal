const BASE_URL = import.meta.env.VITE_API_BASE || ""; // default same origin

export async function predictText(text) {
  const res = await fetch(`${BASE_URL}/api/predict-text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });
  if (!res.ok) throw new Error("Predict text failed");
  return res.json();
}

export async function predictSpeech(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE_URL}/api/predict-speech`, {
    method: "POST",
    body: form
  });
  if (!res.ok) throw new Error("Predict speech failed");
  return res.json();
}
