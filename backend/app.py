import os
import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

load_dotenv()
app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///moodsense.db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'replace_me')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-string')
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_sub = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256))
    name = db.Column(db.String(256))
    picture = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood_label = db.Column(db.String(64))
    mood_score = db.Column(db.Float)
    text = db.Column(db.Text, nullable=True)
    audio_path = db.Column(db.String(512), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Initialize DB route (dev)
@app.route('/api/initdb', methods=['POST'])
def initdb():
    db.create_all()
    return jsonify({'status':'ok'})

# Google auth: accept id_token from frontend, verify and create user + JWT
@app.route('/api/auth/google', methods=['POST'])
def auth_google():
    data = request.get_json(force=True)
    token = data.get('id_token')
    if not token:
        return jsonify({'error':'id_token required'}), 400
    try:
        idinfo = id_token.verify_oauth2_token(token, grequests.Request())
        # idinfo contains 'sub', 'email', 'name', 'picture'
        sub = idinfo['sub']
        user = User.query.filter_by(google_sub=sub).first()
        if not user:
            user = User(google_sub=sub, email=idinfo.get('email'), name=idinfo.get('name'), picture=idinfo.get('picture'))
            db.session.add(user)
            db.session.commit()
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token, 'user': {'id': user.id, 'email': user.email, 'name': user.name, 'picture': user.picture}})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Simple text emotion analyzer (placeholder)
def analyze_text_emotion(text):
    # placeholder logic: refine by using your fine-tuned model later
    text_lower = (text or "").lower()
    if any(w in text_lower for w in ['happy','joy','love','great']):
        return {'label':'happy','score':0.9}
    if any(w in text_lower for w in ['sad','depress','unhappy','tired']):
        return {'label':'sad','score':0.9}
    return {'label':'neutral','score':0.6}

# Save mood endpoint: accepts text payload or audio file
@app.route('/api/chat/message', methods=['POST'])
@jwt_required()
def chat_message():
    user_id = get_jwt_identity()
    data = request.get_json(force=True)
    text = data.get('text')
    # TODO: Integrate your chatbot and model; for now analyze text and save
    mood = analyze_text_emotion(text)
    entry = MoodEntry(user_id=user_id, mood_label=mood['label'], mood_score=mood['score'], text=text)
    db.session.add(entry)
    db.session.commit()
    # generate tailored suggestion (simple)
    suggestions = {
        'happy': 'Great to hear! Keep doing what you love. Try sharing gratitude today.',
        'sad': 'I'm sorry you're feeling down. Try a short breathing exercise or write for 5 minutes.',
        'neutral': 'Try a short walk to refresh your mind.'
    }
    suggestion = suggestions.get(mood['label'], 'Take a short break and do something you enjoy.')
    return jsonify({'mood': mood, 'suggestion': suggestion, 'saved': True})

# Upload audio + analyze
@app.route('/api/mood/upload', methods=['POST'])
@jwt_required()
def upload_audio():
    user_id = get_jwt_identity()
    if 'audio' not in request.files:
        return jsonify({'error':'no audio file'}), 400
    f = request.files['audio']
    filename = f.filename
    upldir = os.path.join('uploads')
    os.makedirs(upldir, exist_ok=True)
    path = os.path.join(upldir, filename)
    f.save(path)
    # TODO: call speech emotion model
    mood = {'label':'sad', 'score':0.7}
    entry = MoodEntry(user_id=user_id, mood_label=mood['label'], mood_score=mood['score'], audio_path=path)
    db.session.add(entry)
    db.session.commit()
    return jsonify({'mood': mood, 'saved': True})

# Get user mood history
@app.route('/api/mood/user', methods=['GET'])
@jwt_required()
def user_moods():
    user_id = get_jwt_identity()
    entries = MoodEntry.query.filter_by(user_id=user_id).order_by(MoodEntry.created_at.desc()).limit(500).all()
    out = [{'id': e.id, 'label': e.mood_label, 'score': e.mood_score, 'text': e.text, 'audio': e.audio_path, 'created_at': e.created_at.isoformat()} for e in entries]
    return jsonify(out)

# Trends across all users
@app.route('/api/mood/trends', methods=['GET'])
def trends():
    # aggregate simple counts per label
    rows = db.session.query(MoodEntry.mood_label, db.func.count(MoodEntry.id)).group_by(MoodEntry.mood_label).all()
    data = {label: int(cnt) for label, cnt in rows}
    return jsonify(data)

# Serve frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build'))
    if path != "" and os.path.exists(os.path.join(root_dir, path)):
        return send_from_directory(root_dir, path)
    if os.path.exists(os.path.join(root_dir, 'index.html')):
        return send_from_directory(root_dir, 'index.html')
    return jsonify({'status':'backend running'})

if __name__ == '__main__':
    # create DB if not exists (dev convenience)
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
