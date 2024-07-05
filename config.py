from decouple import config
from dotenv import load_dotenv
from dataclasses import dataclass
from enum import Enum

load_dotenv()


@dataclass
class Config:
    # MISTRAL_API_KEY = config('MISTRAL_API_KEY')
    # MISTRAL_MODEL_NAME = config('MISTRAL_MODEL_NAME')
    VECTOR_DB_PATH = config('VECTOR_DB_PATH')
    SLACK_WEBHOOK_URL = config('SLACK_WEBHOOK_URL')
    OPENAI_API_KEY = config('OPENAI_API_KEY')
    OPENAI_MODEL_NAME = config('OPENAI_MODEL_NAME')