# OpenRouter Reasoning Web App & CLI
# IAN - Intelligent Assistant Navigator	A smart guide that helps you find answers and stay on track.
This project allows you to test out OpenRouter reasoning models (like `openai/gpt-oss-120b:free` or DeepSeek R1 models) using both a Web App and a CLI interface. 

## Prerequisites
- Python 3.8+ installed on your system.

### How to Install Python
- **Windows**: Download the installer from the [official Python website](https://www.python.org/downloads/). Check the box **"Add python.exe to PATH"** at the bottom of the installer window before clicking "Install Now".
- **macOS**: Download the macOS installer from the official website, or install via Homebrew: `brew install python`.
- **Linux**: Run `sudo apt update && sudo apt install python3 python3-venv python3-pip` (on Ubuntu/Debian) to ensure it is installed.

## Setup Instructions

1. **Install Dependencies**
   Open your terminal/command prompt in the project directory and install the required Python packages:
   ```cmd
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   - Copy the `.env.example` file and rename it to `.env`.
   - Open `.env` and paste your OpenRouter API key inside:
     ```env
     OPENROUTER_API_KEY=your_api_key_here
     MODEL_NAME=openai/gpt-oss-120b:free
     ```
   *(You can also adjust the `MODEL_NAME` to any OpenRouter model that supports reasoning capabilities if you wish.)*

## How to Run

### Option 1: Web Application (Recommended)
This features a clean, responsive, dark-mode user interface where you can see the AI's response (and its internal reasoning process if you previously modified it to show).
- **Run via Script**: Double-click the `run.bat` file in your folder, or run `.\run.bat` in your terminal.
- **Run via Python**: Run `python app.py` in your terminal.
- **Access the App**: Once it is running, open your browser and navigate to `http://127.0.0.1:5000`.

### Option 2: CLI (Command Line Interface)
If you prefer a fast, terminal-only chat session:
- Run `python main.py` in your terminal.
- Type your prompt and press Enter. The CLI will display the thought process (`Reasoning:`) followed by the final answer (`Assistant:`).
- Type `quit` or `exit` to end the session.
