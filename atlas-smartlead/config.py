
import os
from dotenv import load_dotenv

# .env dosyasındaki ayarları yükle
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "local-development-key")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "atlas.db")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
