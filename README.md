# SleepOnCall
A discord bot that disconnects you from a voice channel after a period of time.

You can happily fall asleep on call without worrying that being on call throughout the night drains your phone battery.

## Usage

The bot is currently hosted (but possibly unreliably) with free services.
Click [here](https://discord.com/oauth2/authorize?client_id=1240967966040916049) to invite into your server.

The bot uses slash commands. Discord will prompt for the valid commands for the bot when you type `/`.

## Setup & Installation

### Create bot

1. Created a Discord bot on [Discord Developer Portal](https://discord.com/developers/applications)
2. Under **Installation**, set up the *Install Link* and give the following permissions:
    - Connect
    - Send Message
3. Under **Bot**, generate (or reset) a *TOKEN* and keep it safe, you will need it later 

### Configure bot

In `config.py`, you can set some confiugration. These configuration have default values
and you can choose not to change them.

You can configure the following:
  -  `MAX_TIMER`
     - Maximum time which the bot shall accept.
       Time refers how long to wait before disconnecting user.
     - Format: `(sec, min, hrs)`
     - Default: `(0, 0, 2)` = 2 hours, 0 min, 0 sec
  -  `MENTION_USER`
      - Mention(tag) user when a request is confirmed/aborted.
      - Options: `True` (Default) or `False`
  -  `ALLOW_PROXY`
     - Allow admin/mods/(users with required permissions) to disconnect target user.
     - Options: `True` (Default) or `False`

### Run bot locally

#### Dependencies

- [Python](https://www.python.org/) with [Pip](https://pip.pypa.io/en/stable/installation/)

#### Steps

1. Create a `.env` file
2. In the `.env` file, add the Discord bot token
   ```
   BOT_TOKEN="Your Bot Token Generated When Creating Bot"
   ```
3. Install dependencies stated in `requirements.txt`
   ```
   pip install -r requirements.txt
   ```
4. Run `main.py`
   ```
   python main.py
   ```

### Adding bot to server

1. Enter the *Install Link* into your broswer
   > If *Install Link* is a *Discord Provided Link* it should look like `https://discord.com/oauth2/authorize?client_id=xxx`
2. Sign into your Discord account
3. Select the server to add the bot into, then click `Continue`
4. Check all required permissions (should be checked by default), then click `Authorise`
5. Bot is now added to server