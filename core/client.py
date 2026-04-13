from openai import OpenAI
from config.settings import OPENROUTER_API_KEY, BASE_URL

def get_client() -> OpenAI:
    return OpenAI(
        base_url=BASE_URL,
        api_key=OPENROUTER_API_KEY,
    )