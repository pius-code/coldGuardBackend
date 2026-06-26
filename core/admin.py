import os
from dotenv import load_dotenv

load_dotenv()

# TODO: use db to store ids and add privileges to it
_raw = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [aid.strip() for aid in _raw.split(",") if aid.strip()]
