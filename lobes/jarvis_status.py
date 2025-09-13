import discord
import os
import requests
import logging
import subprocess
import psutil

from discord.ext import commands
from discord import app_commands

logging.basicConfig(
    filename=r'C:\Users\immor\Desktop\J.A.R.V.I.S\logs\jarvis_report.log',
    filemode='w',
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def find_pid_by_name(name: str):
    pids = []
    for process in psutil.process_iter(['pid', 'name']):
        try:
            if name.lower() in process.info['name'].lower():
                pids.append(process.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return pids

class Jarvisstatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='jarvis_status', description='turn on or off mythomax ai for jarvis BREEZY ONLY')
    @app_commands.choices(ai_status=[
        app_commands.Choice(name='On', value="On"),
        app_commands.Choice(name='Off', value="Off")
    ])
    async def jarvis_status(self, interaction: discord.Interaction, ai_status: str):
        await interaction.response.defer(thinking=True)

        if interaction.user.id == 1340871053173456976:
            if ai_status == 'Off':

                if find_pid_by_name('koboldcpp'):
                    try:
                        for pid in find_pid_by_name('koboldcpp'):
                            subprocess.call(["taskkill", "/F", "/PID", str(pid)])
                        await interaction.followup.send('Killed process successfully sir,')
                    except Exception as e:
                        await interaction.followup.send(f'I couldn\'t kill the process sir,')

                else:
                    await interaction.followup.send('The AI wasn\'t running sir,')

            elif ai_status == 'On':
                subprocess.Popen([r"C:\Users\immor\Desktop\J.A.R.V.I.S\jarvis voice\start_koboldbat.vbs"], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                await interaction.followup.send('I am listening sir,')
        else:
            await interaction.followup.send('You\'re not authorized to do that sir,')





async def setup(bot):
    await bot.add_cog(Jarvisstatus(bot))