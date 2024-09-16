# SleepOnCall
A discord bot that disconnects you from a voice channel after a period of time.

You can happily fall asleep on call without worrying that being on call throughout the night drains your phone battery.

## Running bot locally

Pre-requisite: created a Discord bot on [Discord Developer Portal](https://discord.com/developers/applications).

1. Create a `.env` file
2. In the `.env` file, add the Discord bot token
   ```
   BOT_TOKEN="ADD_YOUR_OWN_DISCORD_BOT_TOKEN_HERE"
   ```
3. Install dependencies stated in `requirements.txt`
   ```
   pip install -r requirements.txt
   ```
4. Run `main.py`
   ```
   python main.py
   ```