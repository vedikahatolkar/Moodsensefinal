#!/bin/bash
# Run once in Codespaces terminal to setup backend env and run
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
flask run --host=0.0.0.0
