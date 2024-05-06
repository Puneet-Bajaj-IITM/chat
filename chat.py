from flask import Flask, request, session, jsonify, send_from_directory
from chat_utils import load_folder, load_db, custom_prompt
from flask_session import Session
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from flask_sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__)


# Set a secret key for session management
app.secret_key = b'SECRET_KEY'
UPLOAD_FOLDER = 'uploads'
SESSION_TYPE = 'filesystem'
SESSION_FOLDER = 'flask_session'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_FILE_DIR'] = SESSION_FOLDER
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_TYPE'] = SESSION_TYPE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///session_data.db'

llm_service = "groq"
system_message = "You are a helpful customer support assistant for a website. Give answer of each question in as brief as possible"
groq_llm_name = "mixtral-8x7b-32768"
openai_llm_name = "gpt-3.5-turbo"
temperature = 0
k = 5
chunk_size=1000
chunk_overlap=200
chat = None

app.config.from_object(__name__)
Session(app)
db = SQLAlchemy(app)

from manager.session_manager import *

with app.app_context():
    db.create_all()

def initialize_llm():
    global chat
    if os.path.exists(".env"):
        from dotenv import load_dotenv
        load_dotenv()
        if os.getenv('GROQ_API_KEY') and llm_service == "groq":
            chat = ChatGroq(temperature=temperature, groq_api_key=os.getenv('GROQ_API_KEY'), model_name=groq_llm_name)
        elif os.getenv('OPENAI_API_KEY') and llm_service == "openai":
            chat = ChatOpenAI(model='gpt-3.5-turbo')
    else:
        chat = ChatGroq(temperature=temperature, model_name=openai_llm_name)

initialize_llm()

@app.after_request
def add_cors_headers(response):
    """Add CORS headers to allow cross-origin requests."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
    return response

# docs = load_folder('uploads')
# vectordb = load_db(docs)
docs = None
vectordb = None

if __name__ == '__main__':
    with app.app_context():
        sessions = SessionData.query.all()
    with app.app_context():
        db.create_all()
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    from routes.document_routes import *
    from routes.llm_routes import *
    from routes.session_routes import *

    app.run(debug=True)
