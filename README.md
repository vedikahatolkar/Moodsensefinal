# MoodSense — Full-stack scaffold (React + Flask)

This repo is a scaffold for the MoodSense app (React frontend + Flask backend). It includes:
- Google Sign-in (OIDC) flow (frontend collects id_token and backend verifies).
- Chatbot UI (text + audio upload) that saves mood entries to DB with timestamp.
- User dashboard with mood history and simple charts (Chart.js).
- Trends page aggregating moods across users.
- Scripts for downloading/fine-tuning text (GoEmotions) and speech (RAVDESS) datasets.
- Docker + docker-compose for local development.

Important next steps:
1. Create a Google OAuth Client ID (Web application) and set the Frontend `REACT_APP_GOOGLE_CLIENT_ID` in `frontend/.env`.
2. For production, configure HTTPS and secure cookies.
3. Replace placeholder ML models with your fine-tuned checkpoints.

See each folder for usage instructions.

