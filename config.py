import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
MAX_TIMER = (0, 0, 2) # 0 sec, 0 min, 2 hours
COMMERCIAL = False
