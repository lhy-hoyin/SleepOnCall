import discord

requests = {} # {user: timer}

def add_request(user: discord.Member, timer: int):
    requests[user] = timer

def get_requests_copy():
    return requests.copy()

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
