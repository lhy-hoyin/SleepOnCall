import discord
from typing import TypedDict
from discord.ext import tasks
from helper import time_in_str, time_in_seconds
from config import MAX_TIMER

RequestDict = TypedDict('Request', {'user': discord.Member, 'timer': int})
requests = RequestDict()

@tasks.loop(seconds=1)
async def logic_loop():
    for user, timer in requests.copy().items():
        # User has left vc on their own
        if not user.voice:
            remove_request(user)
            continue
        
        # Timer has ended
        if timer <= 0:
            await disconnect_user(user)
            remove_request(user)
            continue
        
        # Update with a reduced timer
        add_request(user, timer - 1)
    
    # Stop logic loop if no more pending requests
    if len(requests) == 0:
        logic_loop.stop()

def add_request(user: discord.Member, timer: int):
    requests[user] = timer

def check_request(user: discord.Member) -> int | None:
    if user in requests:
        return requests[user]

def remove_request(user: discord.Member) -> bool:
    if user in requests:
        del requests[user]
        return True
    else:
        return False

async def disconnect_user(user: discord.Member) -> bool:
    if user.voice:
        await user.move_to(None)
        return True
    else:
        return False

async def handle_disconnect_request(interaction: discord.Interaction, timer):
    requester = interaction.user
    
    # User not connected to voice channel
    if requester.voice is None:
        await interaction.response.send_message(
            content='You are not in any voice channel.',
            delete_after=10,
            ephemeral=True)
        return

    # Requested time exceed max time limit
    if timer > time_in_seconds(MAX_TIMER):
        await interaction.response.send_message(
            content=f'Request time exceeds max time limit.\nMax is {time_in_str(time_in_seconds(MAX_TIMER))}.',
            ephemeral=True)
        return
    
    # Requested time is "over", disconnect now
    if timer <= 0:
        await interaction.response.send_message(
            content=f'Disconnecting {requester.display_name}...', silent=True)
        await disconnect_user(requester)
        return

    # Add to requests
    add_request(requester, timer)
    if not logic_loop.is_running():
        logic_loop.start()

    # Acknowledge success of request
    await interaction.response.send_message(
        content=f'{requester.display_name} will be disconnected in {time_in_str(timer)}.\nTo cancel, use </abort:1240892252595818566>.')
