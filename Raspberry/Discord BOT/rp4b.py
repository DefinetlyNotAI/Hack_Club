import json
import os
import platform
import subprocess
import colorlog
import discord
import requests
from datetime import datetime
from discord.ext import commands

# TODO Update readme doc.
# TODO Make the perms in readme
# TODO View Channel
# TODO Create Invite
# TODO Read Message History
# TODO REST IS OFF
# TODO Add option to upload the file to github, etc
# TODO also must explain the reaction symbol meanings


class Log:
    def __init__(self, filename="Server.log", max_size=None):
        """
        Initializes a new instance of the Log class.

        Args:
            filename (str, optional): The name of the log file. Defaults to "Server.log".
            max_size (int, optional): The maximum size of the log file in bytes. Defaults to infinity.

        Initializes the `filename` and `size` attributes of the Log instance.
        If the log file does not exist, it creates an empty file with the specified name.
        """
        # Use the provided filename or default to 'Server.log'
        self.filename = str(filename)
        self.size = int(max_size)

        # Check if the file exists and create it if it doesn't
        if not os.path.exists(self.filename):
            with open(self.filename, "w"):
                pass  # Empty file content is fine here since we append logs

    @staticmethod
    def __timestamp():
        """
        Retrieves the current date and time and formats it into a string timestamp.

        Returns:
            str: A string representing the formatted timestamp.
        """
        # Get the current date and time
        now = datetime.now()

        # Format the timestamp as a string
        time = f"{now.strftime('%Y-%m-%d %H:%M:%S')}"

        return time

    def __remove(self):
        """
        Remove the log file if it exists and the number of lines in the file exceeds the specified size.

        This function checks if the log file specified by the `filename` attribute exists. If it does, it opens the file in read mode and counts the number of lines in the file. If the number of lines is greater than the specified `size`, the file is removed.

        Returns:
            None
        """
        if os.path.exists(self.filename) and self.size is not None:
            with open(self.filename, "r") as file:
                line_count = sum(1 for _ in file)
            if line_count > self.size:
                os.remove(self.filename)

    def info(self, message):
        """
        Writes an information log message to the log file.

        Args:
            message (str): The message to be logged.

        Returns:
            None
        """
        self.__remove()
        with open(self.filename, "a") as f:
            f.write(f"INFO: {message} at {self.__timestamp()}\n")

    def warning(self, message):
        """
        Writes a warning log message to the log file.

        Args:
            message (str): The warning message to be logged.

        Returns:
            None
        """
        self.__remove()
        with open(self.filename, "a") as f:
            f.write(f"WARNING: {message} at {self.__timestamp()}\n")

    def error(self, message):
        """
        Writes an error log message to the log file.

        Args:
            message (str): The error message to be logged.

        Returns:
            None
        """
        self.__remove()
        with open(self.filename, "a") as f:
            f.write(f"ERROR: {message} at {self.__timestamp()}\n")

    def critical(self, message):
        """
        Writes a critical log message to the log file.

        Args:
            message (str): The critical message to be logged.

        Returns:
            None
        """
        self.__remove()
        with open(self.filename, "a") as f:
            f.write(f"CRITICAL: {message} at {self.__timestamp()}\n")


# Configure colorlog for logging messages with colors
log = Log(filename="Discord.log", max_size=2500)
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
    try:
        with open('api.json', 'r') as f:
            config = json.load(f)
        if config is not None and isinstance(config['token'], str) and isinstance(config['channel_id'], int) and isinstance(
                config['webhooks_username'], str) and isinstance(config['should_we_crack_files?'], bool) and isinstance(
                config['limit_of_messages_to_check'], int) and isinstance(config['log_using_debug?'], bool):
            return config['token'], config['channel_id'], config['webhooks_username'], config['should_we_crack_files?'], config['limit_of_messages_to_check'], config['log_using_debug?']
        else:
            colorlog.critical("Invalid JSON file format")
            log.critical("Invalid JSON file format")
            exit(1)
    except Exception as e:
        colorlog.critical(f"Error reading JSON file: {e}")
        log.critical(f"Error reading JSON file: {e}")
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
    colorlog.info(f'We have logged in as {bot.user}')
    log.info(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    colorlog.info(f'Message from {message.author}: {message.content}')
    channel_id = CHANNEL_ID
    await check_old_messages(channel_id)


async def check_old_messages(channel_id):
    channel = bot.get_channel(channel_id)
    if channel is None:
        colorlog.error(f"Channel with ID {channel_id} not found.")
        log.error(f"Channel with ID {channel_id} not found.")
        return

    async for message in channel.history(limit=LIMIT):
        if message.author.name == WEBHOOK_USERNAME:
            for attachment in message.attachments:
                if attachment.filename.endswith('.pcap'):
                    if any(reaction.emoji == '👀' for reaction in message.reactions):
                        colorlog.info("Seen reaction found. Skipping download.")
                        log.info("Seen reaction found. Skipping download.")
                        continue  # Skip this message if the Seen reaction is present
                    name = attachment.filename
                    await download_pcap_file(attachment.url, name)
                    colorlog.info(f'Downloaded {name} from {attachment.url}')
                    log.info(f'Downloaded {name} from {attachment.url}')

                    try:
                        if CRACK:
                            colorlog.info("Attempting to execute cracker.py...")
                            log.info("Attempting to execute cracker.py...")
                            try:
                                # Check for cracker.py in the current directory and download if not found
                                if not os.path.exists('cracker.py'):
                                    colorlog.debug("cracker.py not found locally. Downloading...")
                                    log.info("cracker.py not found locally. Downloading...")
                                    url = "https://raw.githubusercontent.com/DefinetlyNotAI/Hack_Club/main/Raspberry/Discord%20BOT/cracker.py"
                                    response = requests.get(url)
                                    with open("cracker.py", 'wb') as f:
                                        f.write(response.content)
                                    colorlog.info("Downloaded cracker.py")
                                    log.info("Downloaded cracker.py")

                                if platform.system() == 'Windows':
                                    colorlog.error(f"Windows is not supported for cracking. Please use Linux.")
                                    colorlog.warning(
                                        f"You can skip this step by setting 'should_we_crack' to False in api.json.")
                                    log.error(f"Windows attempted to be used for cracking. Failed")
                                    try:
                                        await message.clear_reactions()
                                        colorlog.info(f"Cleared all reactions from message ID {message.id}")
                                        log.info(f"Cleared all reactions from message ID {message.id}")
                                    except Exception as e:
                                        colorlog.error(f"Failed to clear reactions from message ID {message.id}: {e}")
                                        log.error(f"Failed to clear reactions from message ID {message.id}: {e}")
                                    await message.add_reaction('⛔')
                                else:
                                    try:
                                        subprocess.run(['python', 'cracker.py', name], check=True)
                                        colorlog.info("Successfully executed cracker.py.")
                                        log.info("Successfully executed cracker.py.")
                                        try:
                                            await message.clear_reactions()
                                            colorlog.info(f"Cleared all reactions from message ID {message.id}")
                                            log.info(f"Cleared all reactions from message ID {message.id}")
                                        except Exception as e:
                                            colorlog.error(
                                                f"Failed to clear reactions from message ID {message.id}: {e}")
                                            log.error(f"Failed to clear reactions from message ID {message.id}: {e}")
                                        await message.add_reaction('👀')
                                    except Exception as e:
                                        colorlog.error(f"Failed to execute cracker.py: {e}")
                                        log.error(f"Failed to execute cracker.py: {e}")
                                        try:
                                            await message.clear_reactions()
                                            colorlog.info(f"Cleared all reactions from message ID {message.id}")
                                            log.info(f"Cleared all reactions from message ID {message.id}")
                                        except Exception as e:
                                            colorlog.error(
                                                f"Failed to clear reactions from message ID {message.id}: {e}")
                                            log.error(f"Failed to clear reactions from message ID {message.id}: {e}")
                                        await message.add_reaction('👎')
                            except Exception as e:
                                colorlog.critical(f"Unexpected issue occurred: {e}")
                                log.critical(f"Unexpected issue occurred: {e}")
                                try:
                                    await message.clear_reactions()
                                    colorlog.info(f"Cleared all reactions from message ID {message.id}")
                                    log.info(f"Cleared all reactions from message ID {message.id}")
                                except Exception as e:
                                    colorlog.error(f"Failed to clear reactions from message ID {message.id}: {e}")
                                    log.error(f"Failed to clear reactions from message ID {message.id}: {e}")
                                await message.add_reaction('⚠️')
                        else:
                            try:
                                await message.clear_reactions()
                                colorlog.info(f"Cleared all reactions from message ID {message.id}")
                                log.info(f"Cleared all reactions from message ID {message.id}")
                            except Exception as e:
                                colorlog.error(f"Failed to clear reactions from message ID {message.id}: {e}")
                                log.error(f"Failed to clear reactions from message ID {message.id}: {e}")
                            await message.add_reaction('❌')
                    except Exception as e:
                        colorlog.critical(f"Unexpected issue occurred: {e}")
                        log.critical(f"Unexpected issue occurred: {e}")


async def download_pcap_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)


@bot.command(name='logs', help='Sends the Discord.log file to the chat.')
# TODO FIX this
async def send_logs(ctx):
    """
    Sends the contents of the Discord.log file to the chat when the /logs command is invoked.
    """
    # Ensure the file exists before attempting to read it
    if os.path.exists("Discord.log"):
        with open("Discord.log", "r") as file:
            log_contents = file.read()

        # Send the contents of the log file to the chat
        await ctx.send(log_contents)
    else:
        await ctx.send("The Discord.log file does not exist yet.")

bot.run(TOKEN, log_handler=None)
