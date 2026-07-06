import discord
from discord import app_commands

from TimerSelectorModal import TimerSelectorModal
from config import ALLOW_PROXY, MAX_TIMER
from helper import time_in_seconds
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
    @app_commands.describe(timer='seconds until disconnect', member='member to disconnect')
    async def dc(
        interaction: discord.Interaction,
        timer: int = 0,
        member: discord.Member | None = None
    ):
        await handle_disconnect_request(interaction, timer, member)

    @tree.command(name='disconnect_me', description='Set a timer, where you will be disconnect after that.')
    async def disconnect_me(interaction: discord.Interaction):
        await interaction.response.send_modal(TimerSelectorModal())

    @tree.command(name='check', description='Check if you have any pending disconnect request')
    async def check(interaction: discord.Interaction):
        await handle_check_request(interaction)

    @tree.command(name='abort', description='Stop a previously made disconnect request, if any')
    @app_commands.describe(member='abort request for member')
    async def abort_request(
        interaction: discord.Interaction,
        member: discord.Member | None = None
    ):
        await handle_abort_request(interaction, member)
    
    if ALLOW_PROXY:
        @tree.command(name='dc-all', description='Disconnect everyone in the current voice channel')
        @app_commands.describe(timer='seconds until disconnect')
        async def dc_all(interaction: discord.Interaction, timer: int = 0):
            await handle_disconnect_all_request(interaction, timer)

    class SleepGroup(app_commands.Group):
        def __init__(self):
            super().__init__(name='sleep-all')
        
        @app_commands.command(name='5mins', description='Quick command to disconnect all in 5 mins')
        async def sleep_all_in_5mins(self, interaction: discord.Interaction):
            await handle_disconnect_all_request(interaction, 60*5)

        @app_commands.command(name='15mins', description='Quick command to disconnect all in 15 mins')
        async def sleep_all_in_15mins(self, interaction: discord.Interaction):
            await handle_disconnect_all_request(interaction, 60*15)
        
        @app_commands.command(name='30mins', description='Quick command to disconnect all in 30 mins')
        async def sleep_in_30mins(self, interaction: discord.Interaction):
            await handle_disconnect_all_request(interaction, 60*30)

        @app_commands.command(name='1hr', description='Quick command to disconnect all in 1hr')
        async def sleep_all_in_1hr(self, interaction: discord.Interaction):
            await handle_disconnect_all_request(interaction, 60*60)

        @app_commands.command(name='max', description='Quick command to disconnect all in the maximum allowed time')
        async def sleep_all_in_max_timer(self, interaction: discord.Interaction):
            await handle_disconnect_all_request(interaction, time_in_seconds(MAX_TIMER))

    if ALLOW_PROXY:
        tree.add_command(SleepGroup())

    @tree.command(name='help', description='Display help message')
    @app_commands.describe(command='The command to get help for')
    async def help(interaction: discord.Interaction, command: str | None = None):
        help_message = (
            "Here are the available commands:"
            f"\n{fmt_cmd('ping')} - Check for bot's status"
            f"\n{fmt_cmd('dc')} - Quick disconnect"
            f"\n{fmt_cmd('disconnect_me')} - Set a timer to disconnect yourself"
            f"\n{fmt_cmd('check')} - Check if you have any pending disconnect requests"
            f"\n{fmt_cmd('abort')} - Stop a previously made disconnect request"
        )

        if ALLOW_PROXY:
            help_message += (
                f"\n{fmt_cmd('dc-all')} - Disconnect everyone in the current voice channel"
                f"\n`/sleep-all xx` - Quick command to disconnect all in xx duration"
            )

        command = (command or "").lstrip("/").lower()
        match command:
            case "": # Empty str
                pass
            case 'ping':
                help_message = (
                    f"{fmt_cmd('ping')} - Check if bot is online and responding."
                    "\nA response means that the bot is online."
                    "\nIf the commands fails to send or get a response, it means that the bot is offline."
                )
            case 'dc':
                help_message = (
                    f"{fmt_cmd('dc')} - Quick disconnect command."
                    "\n"
                    "\nIf no `timer` is specified, it will disconnect immediately."
                    "\nYou can specify the `timer` duration in seconds, subject to the maximum allowed time."
                )
                if ALLOW_PROXY:
                    help_message += (
                        "\n"
                        "\nYou can also specify a `member` to disconnect them instead of yourself."
                        "\nYou must have the permissions and the member must be in the same voice channel as you."
                        "\nRefer to the member using `@`."
                    )
            case 'dc-all':
                help_message = (
                    f"{fmt_cmd('dc-all')} - Disconnect all members in the voice channel."
                    "\nYou must have the permissions and the bot must be configured to allow it."
                    "\n"
                    "\nIf no `timer` is specified, it will disconnect immediately."
                    "\nYou can specify the `timer` duration in seconds, subject to the maximum allowed time."
                )
            case 'disconnect_me':
                help_message = (
                    f"{fmt_cmd('disconnect_me')} - Opens a popup where you can set the duration."
                    "\nYou can specify the duration in hours, minutes, and seconds (HH:mm:ss), "
                    "subjected to the maximum allowed time."
                )
            case 'check':
                help_message = (
                    f"{fmt_cmd('check')} - Check if you have any pending disconnect requests."
                    "\nIf you have a pending request, it will show the remaining time until the disconnect."
                    "\nOnly you can see the response."
                )
            case 'abort':

                help_message = (
                    f"{fmt_cmd('abort')} - Stop a previously made disconnect request."
                    "\nYou can only abort disconnect requests on yourself."
                )
            case 'sleep-all':
                help_message = (
                    f"`/sleep-all xx` - Quick command to disconnect everyone in xx duration."
                    "\nAvailable options are: `5mins`, `15mins`, `30mins`, `1hr`, `max`."
                )

            case _:
                help_message = (
                    f"Command '{command}' not found. "
                    f"Use {fmt_cmd('help')} to see the list of available commands."
                )

        await interaction.response.send_message(help_message)

    return tree

async def capture_commands_id(tree: app_commands.CommandTree) -> None:
    global _cmds
    captured_commands = await tree.fetch_commands()
    for cmd in captured_commands:
        _cmds[cmd.name] = f'</{cmd.name}:{cmd.id}>'

# Format command
def fmt_cmd(cmd_name: str) -> str:
    if cmd_name not in _cmds:
        print(f"WARN: Command '{cmd_name}' not found in captured commands. Please check that command exists.")
        return f'`/{cmd_name}`'
    return _cmds[cmd_name]
