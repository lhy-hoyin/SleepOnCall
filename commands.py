import discord
from discord import app_commands

from logic import (
    add_request,
    check_request,
    remove_request,
    disconnect_user,
    logic_loop
)

"""
Supported Commands:
 - ping
 - dc
 - disconnect_me
 - check
 - abort_request
"""

def tree(bot) -> app_commands.CommandTree:
    tree = app_commands.CommandTree(bot)

    @tree.command(name='ping', description='Check the bot\'s status')
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(content=f'Hi! I\'m {bot.status}.')

    @tree.command(name='dc', description='Quick disconnect')
    @app_commands.describe(timer='seconds until you are disconnected')
    async def dc(interaction: discord.Interaction, timer: int = 0):
        await handle_disconnect_request(interaction, timer)

    @tree.command(name='disconnect_me', description='Set a timer, where you will be disconnect after that.')
    async def disconnect_me(interaction: discord.Interaction):
        await interaction.response.send_modal(TimerSelector())

    @tree.command(name='check', description='Check if you have any pending disconnect request')
    async def check(interaction: discord.Interaction):
        time_left = check_request(interaction.user)
        # TODO: make time_left user friendly, i.e. hr, min, sec
        msg = f'{time_left}s until you are disconnected.' if time_left else 'You have no pending request.'
        await interaction.response.send_message(content=msg, ephemeral=True)

    @tree.command(name='abort', description='Stop a previously made disconnect request, if any')
    async def abort_request(interaction: discord.Interaction):
        requester = interaction.user

        if remove_request(requester):
            await interaction.response.send_message(f'{requester.display_name} will no longer be disconnected.')
        else:
            await interaction.response.send_message('You do not have any disconnect request.', ephemeral=True)

    # @tree.command(name='sponsor', description='Like this bot? Sponsor me :>')
    # async def sponsor(interaction: discord.Interaction):
    #     pass #TODO

    return tree

class TimerSelector(discord.ui.Modal, title='Disconnect duration'):
    time = discord.ui.TextInput(
        label='Time (max 8 hours)',
        placeholder = 'h:mm:ss',
        style=discord.TextStyle.short,
        required=True,
        min_length=5,
        max_length=7
    )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        input = self.time.value

        if input.count(':') != 2:
            return False        

        hrs, min, sec = [int(x) for x in input.split(':')]

        if hrs > 8 or min > 59 or sec > 59 \
            or hrs < 0 or min < 0 or sec < 0:
            return False

        self.time_in_sec = (hrs * 3600) + (min * 60) + sec

        if self.time_in_sec > 28800: # 28800s = 8hrs
            return False

        return True

    async def on_submit(self, interaction: discord.Interaction):
        await handle_disconnect_request(interaction, self.time_in_sec)

async def handle_disconnect_request(interaction: discord.Interaction, timer):
    requester = interaction.user
    
    if requester.voice is None:
        await interaction.response.send_message(
            content='You are not in any voice channel.',
            delete_after=10,
            ephemeral=True)
        return

    if timer <= 0:
        await interaction.response.send_message(
            content='Disconnecting ...',
            delete_after=1,
            ephemeral=True,
            silent=True)
        await disconnect_user(requester)
        return    

    # Add to requests
    add_request(requester, timer)
    if not logic_loop.is_running():
        logic_loop.start()

    # Acknowledge success of request
    # TODO: make time_left user friendly, i.e. hr, min,sec
    await interaction.response.send_message(
        content=f'You will be disconnected in {timer} second(s).\nTo cancel, use `/abort`.',
        delete_after=timer,
        ephemeral=True)
