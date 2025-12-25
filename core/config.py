import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/kasparro"
)

COINPAPRIKA_API_KEY = os.getenv("COINPAPRIKA_API_KEY")
