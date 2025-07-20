# deepseek_client.py
import os
from openai import OpenAI   # misma librería

from dotenv import load_dotenv
load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"  # 👈 único cambio
)

MODEL = "deepseek-chat"      # deepseek-coder si quieres código