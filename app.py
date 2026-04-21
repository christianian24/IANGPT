import sys
import logging
from flask import Flask, render_template, request, jsonify
from core.chat import ReasoningChatSession
from core.database import create_session, get_sessions, get_messages, update_message, delete_messages_after, delete_session, delete_all_sessions, update_session_title
from utils.logger import logger

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    search_query = request.args.get('q', '')
    sessions = get_sessions(search_query)
    return jsonify({'sessions': sessions})

@app.route('/api/sessions', methods=['POST'])
def new_session():
    # Provide a placeholder title, it will update on first message
    session_id = create_session("New Chat")
    return jsonify({'session_id': session_id})

@app.route('/api/sessions/all', methods=['DELETE'])
def remove_all_sessions():
    try:
        delete_all_sessions()
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error wiping sessions: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/<session_id>', methods=['GET'])
def load_session(session_id):
    messages = get_messages(session_id)
    return jsonify({'messages': messages})

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def remove_session(session_id):
    try:
        delete_session(session_id)
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error deleting session: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
        
    try:
        # Initialize a new ReasoningChatSession for each request to remain stateless
        # It handles DB loading and saving via its constructor and send_message methods.
        chat_session = ReasoningChatSession(session_id=session_id)
    except Exception as e:
        logger.error(f"Initialization Error: {e}")
        return jsonify({'error': 'Backend session failed to initialize. Check API keys.'}), 500
        
    try:
        message = chat_session.send_message(user_message)
        
        reasoning = getattr(message, "reasoning_details", None)
        if not reasoning:
            reasoning = getattr(message, "reasoning", getattr(message, "thought", ""))

        return jsonify({
            'content': message.content or '',
            'reasoning': reasoning if reasoning else str(reasoning) if reasoning is not None else ''
        })
    except Exception as e:
        logger.error(f"Error during API call: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat/edit', methods=['POST'])
def edit_chat():
    data = request.json
    session_id = data.get('session_id')
    message_id = data.get('message_id')
    new_content = data.get('content', '')
    
    if not session_id or not message_id or not new_content:
        return jsonify({'error': 'Missing required fields'}), 400
        
    try:
        update_message(message_id, new_content)
        delete_messages_after(session_id, message_id)
        
        chat_session = ReasoningChatSession(session_id=session_id)
    except Exception as e:
        logger.error(f"Error preparing edit session: {e}")
        return jsonify({'error': 'Failed to process edit.'}), 500
        
    try:
        message = chat_session.regenerate_response()
        
        reasoning = getattr(message, "reasoning_details", None)
        if not reasoning:
            reasoning = getattr(message, "reasoning", getattr(message, "thought", ""))

        return jsonify({
            'content': message.content or '',
            'reasoning': reasoning if reasoning else str(reasoning) if reasoning is not None else ''
        })
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
