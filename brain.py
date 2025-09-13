import os
import logging
import discord
import sys
import subprocess

from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

# load my logger
logging.basicConfig(
    filename='logs/jarvis_report.log',
    filemode='w',
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


# load the variables form the env
load_dotenv(dotenv_path='C:/Users/immor/Desktop/J.A.R.V.I.S/tokens&ids.env')
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_ID = os.getenv('DISCORD_BOT_ID')

logger.info('starting jarvis with these credentials:')
logger.info(f'TOKEN: {TOKEN}')
logger.info(f'BOT_ID: {BOT_ID}')

print('starting jarvis')

# load the .bat that runs mythomax ai
subprocess.Popen([r"C:\Users\immor\Desktop\J.A.R.V.I.S\jarvis voice\start_koboldbat.vbs"], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

# creates discord object with all intents
try:
    bot = commands.Bot(command_prefix=commands.when_mentioned_or(""), intents=discord.Intents.all())
except Exception as e:
    logging.error(f'something went wrong when loading the bot object, {e}')
    print(f'we\'ve run into a problem sir,\n{e}')
    sys.exit()

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):

    logger.error(f"Something went wrong with a slash command: {error}")

    # Handle specific errors
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.followup.send(
            "You seem to lack the permissions to run that command.",
            ephemeral=True
        )
    else:
        await interaction.followup.send(
            "Something went wrong sir, I have no clue what.",
            ephemeral=True
        )

# ____________________
# | HELPER FUNCTIONS |
# |__________________|

# empty

# _____________
# | END FUNCS |
# |___________|

# ________________
# |   COMMANDS   |
# |______________|

@app_commands.checks.has_permissions(administrator=True)
@bot.tree.command(name= 'resync', description='sync all my commands')
@app_commands.choices(do_global_sync=[
    app_commands.Choice(name='True', value="True"),
    app_commands.Choice(name='False', value="False")
])
async def resync(interaction: discord.Interaction, do_global_sync: app_commands.Choice[str]):
    await interaction.response.defer(thinking=True)

    if do_global_sync.value == 'True':
        logger.info('starting to sync commands for all servers')
        await interaction.followup.send('I\'m syncing your commands now sir')
        try:
            await bot.tree.sync()
            logger.info('jarvis has synced with all guilds')
            await interaction.followup.send('jarvis has synced with all guilds')
        except Exception as e:
            logger.error(f'Something appears to have went wrong when syncing commands sir, {e}')
            await interaction.followup.send('Something appears to have went wrong when syncing commands sir,')
    else:
        DEV_GUILD_ID = int(os.getenv("DEV_GUILD_ID", "1345760072776679495"))
        DEV_GUILD = discord.Object(id=DEV_GUILD_ID)
        bot.tree.clear_commands(guild=DEV_GUILD)
        await bot.tree.sync(guild=DEV_GUILD)
        await interaction.followup.send('jarvis has synced with dev guild')


for command in bot.tree.walk_commands():
    logger.info(f'registered command: {command.name}')

# ______________________
# |  END OF COMMANDS   |
# |____________________|

@bot.event
async def on_message(message: discord.Message):
    if message.author.id == int(BOT_ID) and message.content == '':
        return
    else:
        if message.author.id == 1340871053173456976:
            if message.content.startswith('jarvis, log this guy'):
                user = bot.get_user(message.mentions[0].id)
                member = message.mentions[0]

                await message.channel.send(
                    f'[]user id: {user.id}\n'
                    f'[]user name: {user.name}\n'
                    f'[]user global_name: {user.global_name}\n'
                    f'[]user display_name: {user.display_name}\n'
                    f'[]user bot_account: {user.bot}\n'
                    f'[]user avatar: {user.avatar}\n\n'
                    
                    f'[]user guild: {member.guild.name}\n'
                    f'[]user join_date: {member.joined_at}\n'
                    f'[]user permissions: {member.guild_permissions}\n'
                    f'[]user nickname: {member.nick}\n'
                    f'[]user top_role: {member.top_role}\n'
                )


@bot.event
async def on_ready():
    logger.info('jarvis has connected to discord')
    logger.info('starting to sync commands for all servers')


    for filename in os.listdir('./lobes'): # loads all cogs
        if filename.endswith('.py'):
            await bot.load_extension(f'lobes.{filename[:-3]}')
            logger.info(f'loaded cog {filename[:-3]}')

    try:
        DEV_GUILD_ID = int(os.getenv("DEV_GUILD_ID", "1345760072776679495"))
        DEV_GUILD = discord.Object(id=DEV_GUILD_ID)
        bot.tree.copy_global_to(guild=DEV_GUILD)
    except Exception as e:
        logging.error(f'Something has gone wrong sir, {e}')
        sys.exit()

    await bot.tree.sync()

    print('I am online sir,')

bot.run(TOKEN)