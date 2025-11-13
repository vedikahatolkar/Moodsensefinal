Backend README

1. Create virtualenv and install:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Create .env in backend/ with:
   FLASK_ENV=development
   SECRET_KEY=replace_me
   DATABASE_URL=sqlite:///moodsense.db

3. Run:
   flask run --host=0.0.0.0

Endpoints:
- POST /api/auth/google  { id_token }  -> returns JWT access token and user profile
- POST /api/chat/message  (auth)       -> Send chat message or text; returns bot reply & saves mood
- POST /api/mood/upload   (auth, form audio) -> Upload audio, analyze, save mood
- GET  /api/mood/user     (auth)       -> returns user mood history
- GET  /api/mood/trends   (auth)       -> aggregated trends

