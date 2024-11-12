import discord
import commands
from config import TOKEN

# Initialise bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    tree = commands.tree(bot)
    await tree.sync()
    await commands.capture_commands_id(tree)
    print(f'REPORT: In {len(bot.guilds)} guild(s).')
    print(f'SUCCESS: {bot.user} is now up and running.')

# Start bot
if TOKEN:
    bot.run(TOKEN)
else:
    print('ERROR: Missing token, cannot run bot')
