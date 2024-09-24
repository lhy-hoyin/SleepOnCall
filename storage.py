import discord
from typing import TypedDict

RequestDict = TypedDict('Request', {'user': discord.Member, 'timer': int})
requests = RequestDict()

def add_request(user: discord.Member, timer: int) -> None:
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

def requests_count() -> int:
    return len(requests)

def get_requests_copy():
    return requests.copy()
