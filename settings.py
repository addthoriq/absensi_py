import os

if os.environ.get("ENVIRONMENT") != "prod":
    from dotenv import load_dotenv
    load_dotenv()

# Environment
ENVIRONMENT = os.environ.get("ENVIRONMENT")

# Fast API Root Path
ROOT_PATH = os.environ.get("ROOT_PATH", "")
