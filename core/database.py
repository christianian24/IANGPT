import sqlite3
import uuid
import datetime
from pathlib import Path
from utils.logger import logger

DB_PATH = Path(__file__).parent.parent / "chat_history.db"

def get_connection():
    """Returns a dictionary-like sqlite connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT,
                    reasoning TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
                )
            ''')
            conn.commit()
    except Exception as e:
        logger.error(f"Error initializing DB: {e}")

def create_session(title="New Chat") -> str:
    session_id = str(uuid.uuid4())
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO sessions (id, title, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
                (session_id, title)
            )
            conn.commit()
    except Exception as e:
        logger.error(f"Error creating session: {e}")
    return session_id

def get_sessions(search_query=None):
    try:
        with get_connection() as conn:
            if search_query:
                # Basic search using LIKE, only return sessions that have messages
                cursor = conn.execute(
                    "SELECT * FROM sessions WHERE title LIKE ? AND EXISTS (SELECT 1 FROM messages WHERE messages.session_id = sessions.id) ORDER BY updated_at DESC", 
                    (f"%{search_query}%",)
                )
            else:
                cursor = conn.execute("SELECT * FROM sessions WHERE EXISTS (SELECT 1 FROM messages WHERE messages.session_id = sessions.id) ORDER BY updated_at DESC")
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error fetching sessions: {e}")
        return []

def update_session_title(session_id: str, title: str):
    try:
        with get_connection() as conn:
            conn.execute(
                "UPDATE sessions SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (title, session_id)
            )
            conn.commit()
    except Exception as e:
        logger.error(f"Error updating session title: {e}")

def get_messages(session_id: str):
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM messages WHERE session_id = ? ORDER BY created_at ASC",
                (session_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error fetching messages: {e}")
        return []

def save_message(session_id: str, role: str, content: str, reasoning: str = None):
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO messages (session_id, role, content, reasoning, created_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                (session_id, role, content, reasoning)
            )
            conn.execute(
                "UPDATE sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (session_id,)
            )
            conn.commit()
    except Exception as e:
        logger.error(f"Error saving message: {e}")

def update_message(message_id: int, content: str):
    try:
        with get_connection() as conn:
            conn.execute(
                "UPDATE messages SET content = ? WHERE id = ?",
                (content, message_id)
            )
            conn.commit()
    except Exception as e:
        logger.error(f"Error updating message: {e}")

def delete_messages_after(session_id: str, message_id: int):
    try:
        with get_connection() as conn:
            conn.execute(
                "DELETE FROM messages WHERE session_id = ? AND id > ?",
                (session_id, message_id)
            )
            conn.execute(
                "UPDATE sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (session_id,)
            )
            conn.commit()
    except Exception as e:
        logger.error(f"Error deleting messages after {message_id}: {e}")

def delete_session(session_id: str):
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
            conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
            conn.commit()
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {e}")

def delete_all_sessions():
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM messages")
            conn.execute("DELETE FROM sessions")
            conn.commit()
    except Exception as e:
        logger.error(f"Error wiping all sessions: {e}")

# Initialize the db on import
init_db()
