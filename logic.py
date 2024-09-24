import discord
from discord.ext import tasks
from helper import time_in_str, time_in_seconds
from config import MAX_TIMER, MENTION_USER, ALLOW_PROXY
from storage import (
    add_request,
    check_request,
    remove_request,
    requests_count,
    get_requests_copy
)

@tasks.loop(seconds=1)
async def logic_loop():
    for user, timer in get_requests_copy().items():
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
    if requests_count() == 0:
        logic_loop.stop()

async def disconnect_user(user: discord.Member) -> bool:
    if user.voice:
        await user.move_to(None)
        return True
    else:
        return False

async def handle_disconnect_request(interaction: discord.Interaction, timer, target: discord.Member):
    requester = interaction.user
    target = requester if target == None else target
    name = f'<@{target.id}>' if MENTION_USER else f'{target.display_name}'

    # Check if requester has permission to disconnect others
    self_request = requester.id == target.id
    has_permission = requester.resolved_permissions.move_members
    if not self_request and not (ALLOW_PROXY and has_permission):
        await interaction.response.send_message(
            content=f'You do not have permission to disconnect {target.display_name}.',
            ephemeral=True)
        return

    # Target user is not connected to voice channel
    if target.voice is None:
        await interaction.response.send_message(
            content=f'{target.display_name} is not in any voice channel.',
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
        await interaction.response.send_message(content=f'Disconnecting {name} ...', silent=True)
        await disconnect_user(target)
        return

    # Add to requests
    add_request(target, timer)
    if not logic_loop.is_running():
        logic_loop.start()

    # Acknowledge success of request
    await interaction.response.send_message(
        content=f'{name} will be disconnected in {time_in_str(timer)}.\nTo cancel, use </abort:1240892252595818566>.')

async def handle_check_request(interaction: discord.Integration):
    time_left = check_request(interaction.user)
    await interaction.response.send_message(
        content=f'{time_in_str(time_left)} until you are disconnected.' if time_left else 'You have no pending request.', 
        ephemeral=True)

async def handle_abort_request(interaction: discord.Integration, target: discord.Member):
    requester = interaction.user
    target = requester if target == None else target
    name = f'<@{target.id}>' if MENTION_USER else f'{target.display_name}'

    # Check if requester has permission to disconnect others
    self_request = requester.id == target.id
    has_permission = requester.resolved_permissions.move_members
    if not self_request and not (ALLOW_PROXY and has_permission):
        await interaction.response.send_message(
            content=f'You do not have permission to abort disconnecting {target.display_name}.',
            ephemeral=True)
        return

    if remove_request(target):
        await interaction.response.send_message(f'{name} will no longer be disconnected.')
    else:
        await interaction.response.send_message(f'{name} do not have any disconnect request.', ephemeral=True)
