import os
import sys
import threading
import time
import webview
from app import app

# Configuration
WINDOW_TITLE = 'IAN GPT Assistant'
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
PORT = 5000
HOST = '127.0.0.1'

def start_flask():
    """Starts the Flask server in a background thread."""
    try:
        # Disable the reloader and debugger for the integrated desktop app
        app.run(host=HOST, port=PORT, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Failed to start Flask server: {e}")

def main():
    # 1. Start Flask in a daemon thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # 2. Give the server a moment to start
    time.sleep(1)

    # 3. Create and start the webview window
    # The URL points to our local Flask server
    url = f'http://{HOST}:{PORT}'
    
    print(f"Launching desktop window at {url}...")
    
    window = webview.create_window(
        WINDOW_TITLE, 
        url,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        min_size=(800, 600)
    )
    
    # window.start() is blocking until the window is closed
    webview.start()

if __name__ == '__main__':
    main()
