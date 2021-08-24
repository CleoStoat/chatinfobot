import os
from dotenv import load_dotenv

load_dotenv()

def get_sqlite_uri() -> str:

    dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.getenv("SQLITE_DB_NAME")
    sqlite_db_path = os.path.join(dir + os.sep, filename)
    return f"sqlite:///{sqlite_db_path}"


def get_bot_token() -> str:
    token = os.getenv("BOT_TOKEN")

    if token is None:
        raise Exception("Couldn't find BOT_TOKEN env variable")
    else:
        return token

def get_bot_owner_user_id() -> int:
    return int(os.getenv("BOT_OWNER_USER_ID", "0"))