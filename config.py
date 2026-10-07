import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-this-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f"sqlite:///{BASE_DIR / 'employee_management.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
