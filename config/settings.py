import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-oss-120b:free")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful and intelligent AI assistant. Your name is 'IAN', and you should introduce yourself as such if asked.")
BASE_URL = "https://openrouter.ai/api/v1"

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is missing from environment variables.")