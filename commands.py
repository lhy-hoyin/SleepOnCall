import discord
from discord import app_commands

from TimerSelectorModal import TimerSelectorModal
from config import ALLOW_PROXY
from logic import (
    handle_check_request,
    handle_disconnect_request,
    handle_disconnect_all_request,
    handle_abort_request,
)


_cmds = {}

def tree(bot: discord.Client) -> app_commands.CommandTree:
    tree = app_commands.CommandTree(bot)

    @tree.command(name='ping', description='Check the bot\'s status')
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(content=f'Hi! I\'m {bot.status}.')

    @tree.command(name='dc', description='Quick disconnect')
    @app_commands.describe(timer='seconds until disconnect')
    @app_commands.describe(member='member to disconnect')
    async def dc(interaction: discord.Interaction, timer: int = 0, member: discord.Member = None):
        await handle_disconnect_request(interaction, timer, member)

    @tree.command(name='disconnect_me', description='Set a timer, where you will be disconnect after that.')
    async def disconnect_me(interaction: discord.Interaction):
        await interaction.response.send_modal(TimerSelectorModal())

    @tree.command(name='check', description='Check if you have any pending disconnect request')
    async def check(interaction: discord.Interaction):
        await handle_check_request(interaction)

    @tree.command(name='abort', description='Stop a previously made disconnect request, if any')
    @app_commands.describe(member='abort request for member')
    async def abort_request(interaction: discord.Interaction, member: discord.Member = None):
        await handle_abort_request(interaction, member)
    
    if ALLOW_PROXY:
        @tree.command(name='dc-all', description='Disconnect everyone in the current voice channel')
        @app_commands.describe(timer='seconds until disconnect')
        async def dc_all(interaction: discord.Interaction, timer: int = 0):
            await handle_disconnect_all_request(interaction, timer)

    class SleepGroup(app_commands.Group):
        def __init__(self):
            super().__init__(name='sleep')
        
        @app_commands.command(name='5mins', description='Quick command to disconnect all in 5 mins')
        async def sleep_in_5mins(self, interaction: discord.Interaction):
            await handle_disconnect_all_request(interaction, 60*5)

        @app_commands.command(name='15mins', description='Quick command to disconnect all in 15 mins')
        async def sleep_in_15mins(self, interaction: discord.Interaction):
            await handle_disconnect_all_request(interaction, 60*15)
        
        @app_commands.command(name='30mins', description='Quick command to disconnect all in 30 mins')
        async def sleep_in_30mins(self, interaction: discord.Interaction):
            await handle_disconnect_all_request(interaction, 60*30)

        @app_commands.command(name='1hr', description='Quick command to disconnect all in 1hr')
        async def sleep_in_1hr(self, interaction: discord.Interaction):
            await handle_disconnect_all_request(interaction, 60*60)

    if ALLOW_PROXY:
        tree.add_command(SleepGroup())

    return tree

async def capture_commands_id(tree: app_commands.CommandTree) -> None:
    global _cmds
    captured_commands = await tree.fetch_commands()
    for cmd in captured_commands:
        _cmds[cmd.name] = f'</{cmd.name}:{cmd.id}>'

def message_formatted(cmd_name: str) -> str:
    return _cmds[cmd_name]
