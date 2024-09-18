import discord
from logic import handle_disconnect_request

class TimerSelector(discord.ui.Modal, title='Disconnect duration'):
    time = discord.ui.TextInput(
        label='Time (max 8 hours)',
        placeholder = 'hh:mm:ss',
        style=discord.TextStyle.short,
        required=True,
        min_length=5,
        max_length=8
    )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        input = self.time.value

        if input.count(':') != 2:
            return False        

        try: 
            hrs, min, sec = [int(x) for x in input.split(':')]

            if hrs > 8 or min > 59 or sec > 59 \
                or hrs < 0 or min < 0 or sec < 0:
                return False

            self.time_in_sec = (hrs * 3600) + (min * 60) + sec

            if self.time_in_sec > 28800: # 28800s = 8hrs
                return False
        except ValueError:
            print(f'Error: cannot parse "{input}" to [hrs, min, sec]')
            return False

        return True

    async def on_submit(self, interaction: discord.Interaction):
        await handle_disconnect_request(interaction, self.time_in_sec)
