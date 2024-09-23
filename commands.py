import discord
from discord import app_commands

from TimerSelector import TimerSelector
from config import COMMERCIAL, MENTION_USER
from helper import time_in_str
from logic import (
    check_request,
    remove_request,
    handle_disconnect_request,
)

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
    @app_commands.describe(timer='seconds until you are disconnected')
    async def dc(interaction: discord.Interaction, timer: int = 0):
        await handle_disconnect_request(interaction, timer)

    @tree.command(name='disconnect_me', description='Set a timer, where you will be disconnect after that.')
    async def disconnect_me(interaction: discord.Interaction):
        await interaction.response.send_modal(TimerSelector())

    @tree.command(name='check', description='Check if you have any pending disconnect request')
    async def check(interaction: discord.Interaction):
        time_left = check_request(interaction.user)
        msg = f'{time_in_str(time_left)} until you are disconnected.' if time_left else 'You have no pending request.'
        await interaction.response.send_message(content=msg, ephemeral=True)

    @tree.command(name='abort', description='Stop a previously made disconnect request, if any')
    async def abort_request(interaction: discord.Interaction):
        requester = interaction.user
        name = f'<@{requester.id}>' if MENTION_USER else f'{requester.display_name}'

        if remove_request(requester):
            await interaction.response.send_message(f'{name} will no longer be disconnected.')
        else:
            await interaction.response.send_message(f'{name} do not have any disconnect request.', ephemeral=True)

    if COMMERCIAL:
        # @tree.command(name='sponsor', description='Like this bot? Sponsor me :>')
        # async def sponsor(interaction: discord.Interaction):
        #     #TODO
        pass

    return tree
