import json
import os
import platform
import subprocess
import colorlog
import discord
import requests
from discord.ext import commands

# TODO Make bot give a SEEN reaction, and also make bot only download .pcap's without the SEEN reaction,

# TODO Update readme doc.
# TODO Make the perms in readme
# TODO View Channel
# TODO Create Invite
# TODO Read Message History
# TODO REST IS OFF
# TODO Add option to upload the file to github, etc

# Configure colorlog for logging messages with colors
logger = colorlog.getLogger()

handler = colorlog.StreamHandler()
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red",
    },
)
handler.setFormatter(formatter)
logger.addHandler(handler)


# Function to read secret keys and information from JSON file
def read_key():
    """
    Reads secret keys from a JSON file.

    Returns:
        tuple: A tuple containing the token, channel ID, and webhooks username.
    """
    try:
        with open('api.json', 'r') as f:
            config = json.load(f)
        if config is not None and isinstance(config['token'], str) and isinstance(config['channel_id'], int) and isinstance(
                config['webhooks_username'], str) and isinstance(config['should_we_crack_files?'], bool) and isinstance(
                config['limit_of_messages_to_check'], int) and isinstance(config['log_using_debug?'], bool):
            return config['token'], config['channel_id'], config['webhooks_username'], config['should_we_crack_files?'], config['limit_of_messages_to_check'], config['log_using_debug?']
        else:
            colorlog.critical("Invalid JSON file format")
            exit(1)
    except Exception as e:
        colorlog.critical(f"Error reading JSON file: {e}")
        exit(1)


# All global variables, and required initializations are done here.
TOKEN, CHANNEL_ID, WEBHOOK_USERNAME, CRACK, LIMIT, DEBUG = read_key()
if DEBUG:
    logger.setLevel(colorlog.DEBUG)
else:
    logger.setLevel(colorlog.INFO)
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    """
    Event triggered when the bot is ready.

    This function is a built-in Discord.py event that is called when the bot has finished logging in and setting up.
    It prints a message to the console indicating that the bot has logged in successfully.
    It then calls the check_old_messages function to check for old messages in a specific channel.

    Returns:
        None
    """
    colorlog.info(f'We have logged in as {bot.user}')
    # Assuming you want to check messages in a specific channel ID
    channel_id = CHANNEL_ID  # Replace with your actual channel ID
    await check_old_messages(channel_id)


async def check_old_messages(channel_id):
    """
    Checks old messages in a specific Discord channel for pcap file attachments.

    Parameters:
        channel_id (int): The ID of the Discord channel to check.

    Returns:
        None
    """
    channel = bot.get_channel(channel_id)
    if channel is None:
        colorlog.error(f"Channel with ID {channel_id} not found.")
        return

    async for message in channel.history(limit=LIMIT):  # Adjust limit as needed
        if message.author.name == WEBHOOK_USERNAME:
            for attachment in message.attachments:
                if attachment.filename.endswith('.pcap'):
                    name = attachment.filename
                    await download_pcap_file(attachment.url, name)
                    colorlog.info(f'Downloaded {name} from {attachment.url}')

                    # Attempt to run cracker.py using WSL on Windows or Python on Linux
                    if CRACK:
                        colorlog.info("Attempting to execute cracker.py...")
                        try:
                            # Check for cracker.py in the current directory and download if not found
                            if not os.path.exists('cracker.py'):
                                colorlog.debug("cracker.py not found locally. Downloading...")
                                url = "https://raw.githubusercontent.com/DefinetlyNotAI/Hack_Club/main/Raspberry/Discord%20BOT/cracker.py"
                                response = requests.get(url)
                                with open("cracker.py", 'wb') as f:
                                    f.write(response.content)
                                colorlog.info("Downloaded cracker.py")

                            if platform.system() == 'Windows':
                                colorlog.error(f"Windows is not supported for cracking. Please use Linux.")
                                colorlog.warning(
                                    f"You can skip this step by setting 'should_we_crack' to False in api.json.")
                            else:
                                try:
                                    subprocess.run(['python', 'cracker.py', name], check=True)
                                    colorlog.info("Successfully executed cracker.py.")
                                except Exception as e:
                                    colorlog.error(f"Failed to execute cracker.py: {e}")
                        except Exception as e:
                            colorlog.critical(f"Unexpected issue occurred: {e}")


async def download_pcap_file(url, filename):
    """
    Downloads a pcap file from a given URL and saves it to a specified filename.

    Parameters:
        url (str): The URL of the pcap file to download.
        filename (str): The filename to save the pcap file as.

    Returns:
        None
    """
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)


try:
    bot.run(TOKEN, log_handler=None)
except Exception as e:
    colorlog.error(e)
