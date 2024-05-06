from chat import app
from manager.session_manager import SessionManager
from flask import jsonify

@app.route('/sessions', methods=['GET'])
def get_sessions():
    """Get all previous sessions."""
    sessions = SessionManager.get_sessions_from_db()
    return jsonify(sessions), 200

@app.route('/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get a specific session."""
    session_history = SessionManager.get_sessions_history(session_id)
    if not session_history:
        return jsonify({"error": "Session not found"}), 404
        
    return jsonify(session_history), 200

