import discord
from discord import app_commands

from TimerSelector import TimerSelector
from config import COMMERCIAL
from logic import handle_check_request, handle_disconnect_request, handle_abort_request

"""
Supported Commands:
 - ping
 - dc
 - disconnect_me
 - check
 - abort_request
 - sponsor (not implemented)
"""

def tree(bot: discord.Client) -> app_commands.CommandTree:
    tree = app_commands.CommandTree(bot)

    @tree.command(name='ping', description='Check the bot\'s status')
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(content=f'Hi! I\'m {bot.status}.')

    @tree.command(name='dc', description='Quick disconnect')
    @app_commands.describe(timer='seconds until disconnected')
    @app_commands.describe(member='member to disconnect')
    async def dc(interaction: discord.Interaction, timer: int = 0, member: discord.Member = None):
        await handle_disconnect_request(interaction, timer, member)

    @tree.command(name='disconnect_me', description='Set a timer, where you will be disconnect after that.')
    async def disconnect_me(interaction: discord.Interaction):
        await interaction.response.send_modal(TimerSelector())

    @tree.command(name='check', description='Check if you have any pending disconnect request')
    async def check(interaction: discord.Interaction):
        await handle_check_request(interaction)

    @tree.command(name='abort', description='Stop a previously made disconnect request, if any')
    @app_commands.describe(member='abort request for member')
    async def abort_request(interaction: discord.Interaction, member: discord.Member = None):
        await handle_abort_request(interaction, member)

    return tree
