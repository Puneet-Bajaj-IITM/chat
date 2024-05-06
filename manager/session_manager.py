from chat import db , app
import json

class SessionData(db.Model):
    __tablename__ = 'session_data'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=False)

class SessionManager:
    @staticmethod
    def save_session_data(session_id, data):
        with app.app_context():
            session_data = SessionData.query.filter_by(session_id=session_id).first()
            if session_data:
                session_data.data = json.dumps(data)
            else:
                session_data = SessionData(session_id=session_id, data=json.dumps(data))
                db.session.add(session_data)
            db.session.commit()

    @staticmethod
    def get_sessions_from_db():
        with app.app_context():
            sessions = SessionData.query.all()
            return [session.session_id for session in sessions]
        
    @staticmethod
    def get_sessions_history(session_id):
        with app.app_context():
            session = SessionData.query.filter_by(session_id=session_id).first()
            return json.loads(session.data)
