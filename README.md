# IANGPT

> **I**ntelligent **A**ssistant **N**avigator – A production-ready AI chat application powered by OpenRouter reasoning models.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

IANGPT is a robust, modular web application built with Python and Flask that serves as a sophisticated interface for interacting with large language models. Designed with production-level architecture, it features persistent database-backed chat sessions, seamless contextual messaging, and intelligent model reasoning extraction. The application allows users to edit previous messages, branch conversations, and maintain context effortlessly.

## ✨ Features

- **Persistent Chat Sessions**: Automatically saves and loads chat history using a lightweight SQLite database.
- **Session Management**: Full CRUD support for chat sessions—create, load, rename (automatic upon first message), search, and wipe sessions entirely from a centralized interface.
- **Message Editing**: Robust message editing capabilities with seamless automatic downstream regeneration to maintain conversation logic without manual re-entry.
- **AI Reasoning Extraction**: Built-in backend support to cleanly separate and evaluate the model's internal "thought process" from the final response.
- **Modular Architecture**: Clean separation of concerns with dedicated layers for application routing, core business logic, and utility functions.
- **Structured Error Handling**: Comprehensive server-side logging paired with graceful frontend error states (e.g., rate limits, invalid API keys).
- **Dual Interfaces**: Experience a polished, dark-mode responsive web interface or opt for a fast CLI interface for terminal power-users.

## 🏗 Architecture

The project is structured following RESTful principles and MVC-like separation, emphasizing maintainability and clear data flow:

```text
openrouter-reasoning/
├── app.py                 # Application entry point & REST API routes layer
├── main.py                # Standalone CLI interface for terminal testing
├── requirements.txt       # Project dependencies listing
├── core/                  # Core Business Logic Layer
│   ├── chat.py            # AI Session Handler (ReasoningChatSession)
│   └── database.py        # SQLite interactions, schema & query logic
├── utils/                 # Application Utilities
│   └── logger.py          # Standardized Python logging configuration
├── static/                # Frontend Assets (Vanilla CSS, JS client logic)
└── templates/             # HTML View templates (Jinja)
```

## 🔌 API Endpoint Documentation

The backend adheres to a RESTful architecture, utilizing JSON payloads for seamless frontend integration.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the main web application UI. |
| `GET` | `/api/sessions` | Retrieves all chat sessions (supports `?q=` search filtering). |
| `POST` | `/api/sessions` | Initializes a new chat session in the database. |
| `GET` | `/api/sessions/<id>` | Loads message history for a specific session identifier. |
| `DELETE` | `/api/sessions/<id>` | Deletes a specific user session and its messages. |
| `DELETE` | `/api/sessions/all` | Removes all existing sessions globally. |
| `POST` | `/api/chat` | Submits a new user message to a session and returns AI generation. |
| `POST` | `/api/chat/edit` | Replaces an existing message, prunes subsequent messages, and triggers automated AI regeneration. |

## 🚀 Installation Instructions

### Prerequisites
- Python 3.8 or higher installed.

### Step-by-Step Guide

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/IANGPT.git
   cd IANGPT
   ```

2. **Set Up a Virtual Environment (Recommended)**
   Isolate project dependencies by setting up a local virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Duplicate the example environment block to create your active configuration.
   ```bash
   cp .env.example .env
   ```

## ⚙️ Environment Variable Setup

Open the `.env` file in your preferred text editor and configure the necessary parameters. By default, IANGPT interfaces with OpenRouter.

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
MODEL_NAME=openai/gpt-oss-120b:free
```
*(Note: Replace `your_openrouter_api_key_here` with your actual key. You can swap `MODEL_NAME` for any valid model ID supported by the OpenRouter ecosystem.)*

## 💻 How to Run Locally

### Web Application (Recommended)
Launch the Flask development server to run the primary web user-interface:
```bash
# On Windows, simply double-click run.bat, or execute:
python app.py
```
Once the server is initialized, open your web browser and navigate to `http://127.0.0.1:5000`.

### Command Line Interface (CLI)
If you prefer rapidly testing the model's responses directly from your terminal:
```bash
python main.py
```

## 🔮 Future Improvements

- **User Authentication**: Implement user accounts (e.g., via OAuth or JWT) to provide isolated workspace sessions.
- **Context Pruning Strategies**: Introduce automatic token-aware truncation for accommodating infinitely long contextual conversations without exceeding provider limits.
- **Vector Database Integration (RAG)**: Connect to a Vector Database to augment the model's generations using local, indexed semantic knowledge.
- **WebSocket Streaming Integrations**: Transition from standard HTTP POST requests to WebSockets for real-time, typewriter-style token streaming.
