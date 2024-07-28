import os

if os.environ.get("ENVIRONMENT") != "prod":
    from dotenv import load_dotenv
    load_dotenv()

# Environment
ENVIRONMENT = os.environ.get("ENVIRONMENT")

# Fast API Root Path
ROOT_PATH = os.environ.get("ROOT_PATH", "")

# Connect to PostgreSQL
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

# JWT Config
JWT_PREFIX = os.environ.get("JWT_PREFIX", "Bearer")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
