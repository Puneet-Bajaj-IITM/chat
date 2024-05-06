from chat import app, chat, system_message, vectordb, k, session, openai_llm_name, groq_llm_name, temperature, llm_service, chunk_overlap, chunk_size, initialize_llm
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from manager.session_manager import SessionManager
from chat_utils import custom_prompt
from flask import jsonify, request
import json

@app.route('/query', methods=['GET', 'POST', 'OPTIONS'])
def execute_llm_query():
    """Execute a language model query."""
    if 'messages' not in session:
        global system_message
        session['messages'] = [
            SystemMessage(content=system_message),
        ]
        session['messages_json'] = [
            {"role": "system", "content": system_message},
        ]

    query = request.json.get('userInput')
    global vectordb, k

    prompt_with_rag = query
    # prompt_with_rag , retrieved_data = custom_prompt(vectordb, query, k)

    prompt = HumanMessage(
        content=prompt_with_rag
    )

    session['messages'].append(prompt)
    session['messages_json'].append({"role": "human", "content": prompt_with_rag})
    response = chat.invoke(session['messages']).content.split('</s>')[0]
    session['messages'].append(AIMessage(content=response))
    # session['messages_json'].append({"role": "data_used", "content": retrieved_data})
    session['messages_json'].append({"role": "ai", "content": response})

    session_id = session.sid
    print("Session ID: ", session_id)
    if session_id:
        SessionManager.save_session_data(session_id, session.get('messages_json'))
        print("Session data saved")

    return jsonify({'query': query, 'response': response}), 200

@app.route('/set_llm_params/', methods=['POST'])
def set_llm_params():
    print(f'\n{request.data}\n')
    global openai_llm_name , groq_llm_name, temperature, k, llm_service, system_message, chunk_size, chunk_overlap
    data = request.data.decode('utf-8')
    data_json = json.loads(data)
    system_message = data_json.get('system_message')
    llm_service = data_json.get('llm_service')
    openai_llm_name = data_json.get('openai_llm_name')
    groq_llm_name = data_json.get('groq_llm_name')
    temperature = float(data_json.get('temperature'))
    k = int(data_json.get('k'))
    chunk_size = int(data_json.get('chunk_size'))
    chunk_overlap = int(data_json.get('chunk_overlap'))
    initialize_llm()
    return jsonify({"message": "LLM parameters set successfully"}), 200

@app.route('/get_llm_params/', methods=['GET'])
def get_llm_params():
    global openai_llm_name, groq_llm_name, temperature, k, llm_service, system_message, chunk_size, chunk_overlap
    return jsonify({
        "system_message": system_message,
        "llm_service": llm_service,
        "openai_llm_name": openai_llm_name,
        "groq_llm_name": groq_llm_name,
        "temperature": temperature,
        "k": k,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap
    }), 200