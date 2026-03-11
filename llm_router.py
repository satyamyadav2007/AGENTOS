import os
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI

def get_llm(prefer_local=True):
    if prefer_local:
        try:
            return OllamaLLM(
                model="tinyllama",
                temperature=0.2
            )
        except:
            pass

    return ChatOpenAI(
        model="google/gemini-2.0-flash-exp:free",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
    )