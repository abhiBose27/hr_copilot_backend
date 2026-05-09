import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": os.getenv("APP_URL", "http://localhost:3000"),
        "X-OpenRouter-Title": os.getenv("APP_NAME", "HR Interview Copilot"),
    },
)

TEXT_MODEL = os.getenv("OPENROUTER_TEXT_MODEL", "openai/gpt-4o-transcribe")