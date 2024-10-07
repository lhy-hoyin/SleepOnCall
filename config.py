import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

"""
BOT CONFIGURATIONS
"""

"""
Maximum time which the bot shall accept.
Time refers how long to wait before disconnecting user.
"""
MAX_TIMER = (0, 0, 2) # 0 sec, 0 min, 2 hours

"""
Mention target user (user to be disconnected) when:
- user is instantly disconnected (via bot)
- user is going to be disconnected (by the bot later)
- user is no longer going to be disconnected
"""
MENTION_USER = True

"""
Allow other users (with required permissions) to disconnect target user.
"""
ALLOW_PROXY = True

"""
Use unix timestamp to have Discord show a countdown-style timer to time of disconnect.
Should disable if (hosted) server is found to be inaccurate time
"""
USE_UNIX_TIMESTAMP = True
