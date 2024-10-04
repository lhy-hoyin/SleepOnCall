import discord
from logic import handle_disconnect_request
from helper import time_in_seconds, time_in_str, check_time_bounds
from config import MAX_TIMER

class TimerSelectorModal(discord.ui.Modal, title='Disconnect duration'):
    time = discord.ui.TextInput(
        label=f'Time (max {time_in_str(time_in_seconds(MAX_TIMER))})',
        placeholder = 'hh:mm:ss',
        style=discord.TextStyle.short,
        required=True,
        min_length=5,
        max_length=8
    )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        input = self.time.value

        if input.count(':') != 2:
            print(f'Error: "{input}" is not well formatted')
            return False

        try: 
            hrs, min, sec = [int(x) for x in input.split(':')]
            if not check_time_bounds((sec, min, hrs)):
                print(f'Error: Improper time format "{input}"')
                return False

            self.time_in_sec = time_in_seconds((sec, min, hrs))
            if self.time_in_sec > time_in_seconds(MAX_TIMER):
                print(f'Error: "{input}" exceeds max time limit')
                return False
            
        except ValueError:
            print(f'Error: cannot parse "{input}" to [hrs, min, sec]')
            return False

        return True

    async def on_submit(self, interaction: discord.Interaction):
        await handle_disconnect_request(interaction, self.time_in_sec)
