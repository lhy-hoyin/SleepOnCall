import discord
from discord import app_commands
from discord.ext import tasks

from logic import (
    add_request,
    remove_request,
    pending_requests_count,
    get_requests_copy,
    disconnect_user,
)
from config import TOKEN

# Initialise bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# class TimerSelector(discord.ui.View):
#     def __init__(self, requester):
#         super().__init__()
#         self.user = requester

# class Acknowledgement(discord.ui.View):
#     def __init__(self, time_in_sec: int):
#         super().__init__()  
#         self.timer = time_in_sec

#     @discord.ui.button(label='Abort', style=discord.ButtonStyle.red)
#     async def abort_btn(self, interaction: discord.Interaction, btn: discord.ui.Button):
#         await interaction.response.send_message('Acknowledge', ephemeral=True)

@bot.event
async def on_ready():
    await tree.sync()
    print(f'{bot.user} is now up and running.')

# @discord.ui.button(label='Abort', style=discord.ButtonStyle.red)
# async def abort_btn(interaction: discord.Interaction, btn: discord.ui.Button):
#     await interaction.response.send_message('Acknowledge', ephemeral=True)

@tree.command(name='ping', description='Check the bot\'s status')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(content=f'Hi! I\'m {bot.status}.', ephemeral=True)

@tree.command(name='dc', description='Quick disconnect')
@app_commands.describe(timer='seconds until you are disconnected')
async def dc(interaction: discord.Interaction, timer: int = 0):
    requester = interaction.user

    if requester.voice is None:
        await interaction.response.send_message('You are not in any voice channel.', ephemeral=True)
        return

    if timer <= 0:
        await interaction.response.send_message('Disconnecting ...', ephemeral=True)
        await disconnect_user(requester)
        # await interaction.response.edit_message('Disconnected.', ephemeral=True)
        return    

    # Add to requests
    add_request(requester, timer)
    await interaction.response.send_message(f'You will be disconnected in {timer} second(s).', ephemeral=True)
    
    # TODO: add a abort button
        
    # Start loop if not started
    if not logic_loop.is_running():
        logic_loop.start()

# @tree.command(name='disconnect_me', description='Set a timer, where you will be disconnect after that.')
# async def disconnect_me(interaction: discord.Interaction):
#     pass #TODO

# @tree.command(name='check', description='Check if you have any pending disconnect request')
# async def check(interaction: discord.Interaction):
#     pass #TODO

@tree.command(name='abort', description='Stop a previously made disconnect request, if any')
async def remove_request(interaction: discord.Interaction):
    requester = interaction.user

    if remove_request(requester):
        await interaction.response.send_message(f'{requester.display_name} will no longer be disconnected.')
    else:
        await interaction.response.send_message('You do not have any disconnect request.', ephemeral=True)

# @tree.command(name='sponsor', description='Like this bot? Sponsor me :>')
# async def sponsor(interaction: discord.Interaction):
#     pass #TODO

@tasks.loop(seconds=1)
async def logic_loop():
    for user, timer in get_requests_copy().items():
        if timer > 1:
            add_request(user, timer - 1)
        else:
            await disconnect_user(user)
            remove_request(user)
    
    if pending_requests_count() == 0:
        logic_loop.stop()

# Start bot
if TOKEN:
    bot.run(TOKEN)
else:
    print('ERROR: Missing token, cannot run bot')