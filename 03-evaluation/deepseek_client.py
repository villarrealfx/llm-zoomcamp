import os
from openai import OpenAI 

from dotenv import load_dotenv
load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"  
)

MODEL = "deepseek-chat"      # deepseek-coder para código