import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.chat_models import ChatOllama

load_dotenv()


def get_llm():
    """
    Production-safe hybrid LLM selection.
    Priority:
    1. Groq (cloud, fast, reliable)
    2. Ollama fallback ONLY if Groq key missing
    """

    groq_key = os.getenv("GROQ_API_KEY")

    # --- Use Groq if key exists ---
    if groq_key:
        print("✅ Using Groq LLM")
        return ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=groq_key,
            temperature=0
        )

    # --- Fallback to Ollama ONLY if key missing ---
    print("⚠ GROQ_API_KEY missing → Using Ollama fallback")

    return ChatOllama(
        model="llama3",
        temperature=0
    )
