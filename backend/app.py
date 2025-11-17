from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# load your models (pseudocode)
# from tensorflow.keras.models import load_model
# speech_model = load_model("mood_speech_model.h5")
# text_model = load_model("mood_text_model.h5")

@app.route("/api/predict-text", methods=["POST"])
def predict_text():
    data = request.json
    text = data.get("text", "")
    # run your preprocessing + model -> predicted mood
    # example dummy:
    mood = "neutral"
    confidence = 0.5
    reply = "Thanks for sharing — keep going!"
    return jsonify({"mood": mood, "confidence": confidence, "reply": reply})

@app.route("/api/predict-speech", methods=["POST"])
def predict_speech():
    f = request.files.get("file")
    if not f:
        return jsonify({"error":"no file"}), 400
    # save tmp, run preprocessing, run speech_model.predict(...)
    mood = "happy"
    confidence = 0.95
    reply = "You sound happy — yay!"
    return jsonify({"mood": mood, "confidence": confidence, "reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
