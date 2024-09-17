import discord
from discord.ext import tasks
from typing import TypedDict

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
