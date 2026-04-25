import os
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox

def show_error(title, message):
    """Shows a standard OS error dialog."""
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, message)
    root.destroy()

try:
    import webview
except ImportError:
    show_error("Dependency Error", "The 'pywebview' package is not installed correctly.\nPlease run 'start.bat' to install dependencies.")
    sys.exit(1)

try:
    from app import app
except Exception as e:
    show_error("Startup Error", f"Failed to load the application: {e}")
    sys.exit(1)

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
    # 1. Validate API Key
    if not os.getenv("OPENROUTER_API_KEY"):
        show_error("Configuration Error", "OPENROUTER_API_KEY is missing.\nPlease add it to your .env file.")
        sys.exit(1)

    # 2. Start Flask in a daemon thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # 3. Give the server a moment to start
    time.sleep(1)

    # 4. Create and start the webview window
    url = f'http://{HOST}:{PORT}'
    
    print(f"Launching desktop window at {url}...")
    
    try:
        window = webview.create_window(
            WINDOW_TITLE, 
            url,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            min_size=(800, 600)
        )
        
        webview.start()
    except Exception as e:
        error_msg = str(e)
        if "clr" in error_msg.lower() or "pythonnet" in error_msg.lower():
            show_error("GUI Error", "Failed to initialize the GUI (pythonnet error).\n\nYou likely need the 'Visual Studio Build Tools' installed.\nPlease check the troubleshooting guide in the artifacts folder.")
        else:
            show_error("GUI Error", f"Failed to start the desktop window: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

