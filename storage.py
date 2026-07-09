import discord
from typing import TypedDict, NotRequired

class Request(TypedDict):
    user: discord.Member
    timer: int
    message: NotRequired[str]
    channel: NotRequired[discord.abc.GuildChannel | discord.Thread]

requests: dict[discord.Member, Request] = {}

def add_request(
    user: discord.Member,
    timer: int,
    message: str | None = None,
    channel: discord.abc.GuildChannel | discord.Thread | None = None
) -> None:
    requests[user] = Request(user=user, timer=timer)
    if message and channel:
        requests[user]['message'] = message
        requests[user]['channel'] = channel

def update_request(user: discord.Member, timer: int) -> None:
    if user in requests:
        requests[user]['timer'] = timer

def check_request(user: discord.Member) -> int | None:
    if user in requests:
        return requests[user]['timer']

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
