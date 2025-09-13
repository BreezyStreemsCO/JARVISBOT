import discord
import os
import requests
import logging
import re

from discord.ext import commands
from discord import app_commands

API_URL_mythomax = "http://localhost:5001/api/v1/generate" # mythomax ai generate link

logging.basicConfig(
    filename=r'C:\Users\immor\Desktop\J.A.R.V.I.S\logs\jarvis_report.log',
    filemode='w',
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

last_command_user = False

blacklist_pattern = re.compile(
    r"(security\s*test|debug\s*run|fuzz\s*check|json|qa\s*check|fuzz\s*case)",
    re.IGNORECASE
)

class Talk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='talk_to_jarvis', description='talk with jarvis')
    @app_commands.describe(message='message to enter')
    async def talk(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(thinking=True)

        global last_command_user

        if last_command_user:
            if last_command_user == interaction.user.id:
                await interaction.followup.send('cannot use command twice in a row. let someone else have a turn')
                return

        last_command_user = interaction.user.id

        if re.search(blacklist_pattern, message):
            await interaction.followup.send('contains blacklisted words')
            return

        # generate the prompt adds message later
        with open("prompt.txt", "r") as prompt_text:
            prompt = ""
            prompt += prompt_text.read()

        prompt += f"NOW {interaction.user.name} SPEAKING TO YOU SAYS:\n\n"
        prompt += message + "\n\n"
        prompt += "NOW YOU RESPOND AS JARVIS:"

        try:

            payload = {
                "prompt": prompt,
                "max_length": 2048,
                "temperature": 0.8,
                "top_p": 0.9,
                "top_k": 40,
                "stop_sequence": [""],
                "rep_pen": 1.5,
                "n": 1,
            }

            response = requests.post(API_URL_mythomax, json=payload)
            data = response.json()
            await interaction.followup.send(data['results'][0]['text'])

        except Exception as e:
            logger.info('user tried to talk to jarvis while ai was not running')
            await interaction.followup.send("Jarvis plugged his ears.")

async def setup(bot):
    await bot.add_cog(Talk(bot))