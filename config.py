import os
from dotenv import load_dotenv
from openai import OpenAI

def get_gpt_client():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("❌ OPENAI_API_KEY가 .env 또는 환경변수에 설정되어 있지 않습니다.")
    return OpenAI(api_key=api_key)
