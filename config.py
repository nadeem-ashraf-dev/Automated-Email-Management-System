import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GMAIL_CREDENTIALS_FILE = os.getenv("GMAIL_CREDENTIALS_FILE")
    GMAIL_TOKEN_FILE = os.getenv("GMAIL_TOKEN_FILE")
    GMAIL_USER_EMAIL = os.getenv("GMAIL_USER_EMAIL")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///emails.db")

    POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", 60))