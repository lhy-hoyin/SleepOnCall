import discord
from discord.ext import tasks

requests = {} # {user: timer}

@tasks.loop(seconds=1)
async def logic_loop():
    for user, timer in requests.copy().items():
        if timer > 1:
            add_request(user, timer - 1)
        else:
            await disconnect_user(user)
            remove_request(user)
    
    if pending_requests_count() == 0:
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
    
def pending_requests_count() -> int:
    return len(requests)

async def disconnect_user(user: discord.Member) -> bool:
    if user.voice:
        await user.move_to(None)
        return True
    else:
        return False
