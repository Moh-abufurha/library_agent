from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, sys
from agent import chat
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, "app")

sys.path.append("D:\library_agent\agent.py")



app = Flask(__name__, static_folder=APP_DIR)
CORS(app)

@app.route("/")
def home():
    return send_from_directory(APP_DIR, "index.html")

@app.route("/chat", methods=["POST"])
def chat_api():
    data = request.get_json()
    user_message = data.get("message")
    session_id = data.get("session_id")


    if not session_id:
        session_id = str(uuid.uuid4())

    reply = chat(user_message, session_id=session_id)

    return jsonify({
        "reply": reply,
        "session_id": session_id
    })


if __name__ == "__main__":
    app.run(debug=True)
