import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")