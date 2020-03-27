import os

API_V1_STR = "/api/v1"

PROJECT_NAME = os.getenv("PROJECT_NAME", "Covid")

DB_SERVER = os.getenv("DB_SERVER")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DB = os.getenv("DB_DB")
SQLALCHEMY_DATABASE_URI = (f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_DB}")
