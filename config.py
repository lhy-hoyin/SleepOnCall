import os
from dotenv import load_dotenv

load_dotenv()

# Bot behaviours
MAX_TIMER = (0, 0, 2) # 0 sec, 0 min, 2 hours
MENTION_USER = True

# Bot settings
COMMERCIAL = False
TOKEN = os.getenv('BOT_TOKEN')