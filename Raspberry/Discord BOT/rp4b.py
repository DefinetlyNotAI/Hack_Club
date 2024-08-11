#!/usr/bin/python
# coding:UTF-8

import json
import os
import platform
import shutil
import colorlog
import discord
import requests
from io import BytesIO  # Import BytesIO at the beginning of your script
from discord.ext import commands
from datetime import datetime


# TODO Update readme doc.
#  MUST RUN BY SUDO
#  They can modify the cracker function for their needs as it is not perfect.
#  Include what is still expected (true false returns for error checks etc)(must make a CRACKED directory if not exist and store pcaps there, only generate pcaps)
# TODO Make the perms in readme
#  View Channels
#  Read Message History
#  Send Messages
#  Manage Messages (for clearing reactions)
#  Add Reactions
#  Attach Files
#  Create Invites
#  Link is https://discord.com/oauth2/authorize?client_id=1271825033932832788&permissions=109632&integration_type=0&scope=bot
# TODO also must explain the reaction symbol meanings


class Log:
    def __init__(self, filename="Server.log"):
        """
        Initializes a new instance of the Log class.

        Args:
            filename (str, optional): The name of the log file. Defaults to "Server.log".

        Initializes the `filename` and `size` attributes of the Log instance.
        If the log file does not exist, it creates an empty file with the specified name.
        """
        # Use the provided filename or default to 'Server.log'
        self.filename = str(filename)

        # Check if the file exists and create it if it doesn't
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as log_file:
                log_file.write("|-----Timestamp-----|--Log Level--|-----------------------------------------------------------------------Log Messages-----------------------------------------------------------------------|\n")
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

    def info(self, message):
        """
        Writes an information log message to the log file.

        Args:
            message (str): The message to be logged.

        Returns:
            None
        """
        with open(self.filename, "a") as f:
            f.write(f"[{self.__timestamp()}] > INFO:       {message}\n")

    def warning(self, message):
        """
        Writes a warning log message to the log file.

        Args:
            message (str): The warning message to be logged.

        Returns:
            None
        """
        with open(self.filename, "a") as f:
            f.write(f"[{self.__timestamp()}] > WARNING:    {message}\n")

    def error(self, message):
        """
        Writes an error log message to the log file.

        Args:
            message (str): The error message to be logged.

        Returns:
            None
        """
        with open(self.filename, "a") as f:
            f.write(f"[{self.__timestamp()}] > ERROR:      {message}\n")

    def critical(self, message):
        """
        Writes a critical log message to the log file.

        Args:
            message (str): The critical message to be logged.

        Returns:
            None
        """
        with open(self.filename, "a") as f:
            f.write(f"[{self.__timestamp()}] > CRITICAL:   {message}\n")


# Configure colorlog for logging messages with colors
log = Log(filename="Discord.log")
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
    Attempts to read and parse the 'api.json' file to extract configuration settings.

    The function checks if the file exists, is in the correct format, and contains the required keys. It then returns a tuple containing the extracted configuration values.

    Returns:
        tuple: A tuple containing the extracted configuration values:
            - token (str): The token value from the 'api.json' file.
            - channel_id (int): The channel ID value from the 'api.json' file.
            - webhooks_username (str): The webhooks username value from the 'api.json' file.
            - limit_of_messages_to_check (int): The limit of messages to check value from the 'api.json' file.
            - log_using_debug? (bool): The log using debug value from the 'api.json' file.
    """
    try:
        with open("api.json", "r") as f:
            config = json.load(f)
        if (
            config is not None
            and isinstance(config["token"], str)
            and isinstance(config["channel_id"], int)
            and isinstance(config["webhooks_username"], str)
            and isinstance(config["limit_of_messages_to_check"], int)
            and isinstance(config["log_using_debug?"], bool)
        ):
            return (
                config["token"],
                config["channel_id"],
                config["webhooks_username"],
                config["limit_of_messages_to_check"],
                config["log_using_debug?"],
            )
        else:
            colorlog.critical("Invalid JSON file format")
            log.critical("Invalid JSON file format")
            exit(1)
    except Exception as e:
        colorlog.critical(f"Error reading JSON file: {e}")
        log.critical(f"Error reading JSON file: {e}")
        exit(1)


# All global variables, and required initializations are done here.
TOKEN, CHANNEL_ID, WEBHOOK_USERNAME, LIMIT, DEBUG = read_key()
if DEBUG:
    logger.setLevel(colorlog.DEBUG)
else:
    logger.setLevel(colorlog.INFO)
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    """
    Event handler triggered when the bot is fully connected and ready.

    This function is called when the bot has finished connecting to Discord and
    is ready to start accepting commands and events.

    Parameters:
    None

    Returns:
    None
    """
    colorlog.info(f"We have logged in as {bot.user}")
    log.info(f"We have logged in as {bot.user}")


@bot.event
async def on_message(message):
    """
    Event handler triggered when a message is received, with checks of the author.

    Parameters:
        message (discord.Message): The message object containing information about the message.

    Returns:
        None
    """
    colorlog.info(f"Message from {message.author}: {message.content}")
    log.info(f"Message from {message.author}: {message.content}")

    channel_id = CHANNEL_ID
    if message == "/logs":
        colorlog.info("Uploading logs...")
        await upload_file(message)
    elif message.author == WEBHOOK_USERNAME:
        await extract_and_decrypt(channel_id)
    else:
        colorlog.info(f"Message Ignored due to {message.author} not being {WEBHOOK_USERNAME}")
        log.info(f"Message Ignored due to {message.author} not being {WEBHOOK_USERNAME}")


async def upload_file(ctx, *, message: str = "Here are the logs 🤗"):
    """
    Uploads a file to a specified Discord channel.

    Args:
        ctx: Context object passed by discord.py.
        message: An optional message to accompany the file upload.
    """
    # Retrieve the channel object using the provided channel ID
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        await ctx.send("Channel not found.")
        return

    # Open the file in binary mode and read its content into memory
    with open("Discord.log", "rb") as file:
        file_content = file.read()

    # Create a Discord File object with the file content
    fileToSend = discord.File(file_content, filename="Discord.log")

    # Optionally, send a message with the file
    if message:
        await channel.send(f"{message}\n{fileToSend}")
    else:
        await channel.send(file=fileToSend)


async def extract_and_decrypt(channel_id):
    """
    Extracts and decrypts pcap files from a specified Discord channel.

    This function iterates over the messages in the specified channel, checks for attachments with a .pcap file extension,
    and attempts to download and decrypt them. It also handles reactions and error cases.

    Parameters:
        channel_id (int): The ID of the Discord channel to extract pcap files from.

    Returns:
        None

    This function performs the following steps:
    1. Retrieves the specified channel using the provided channel ID.
    2. Checks if the channel exists, and if not, logs an error and returns.
    3. Iterates over the messages in the channel, starting from the most recent.
    4. For each message, checks if the author is the specified webhook username.
    5. If the author is the specified webhook username, iterates over the attachments of the message.
    6. For each attachment, checks if the file extension is .pcap.
    7. If the file extension is .pcap, checks if the message has a reaction with the emoji '👍'.
    8. If the message has a reaction with the emoji '👍', skips the message and continues to the next one returning to step 3/4.
    9. Downloads the pcap file using the attachment URL and filename.
    10. Logs the download status and filename.
    11. Attempts to crack the pcap file using various tools and techniques.
    12. If cracking is successful, logs the cracked file status and filename.
    13. If cracking fails, logs the failure status and filename.
    14. Adds a reaction to the message based on the cracking result.
    15. Uploads and deletes the cracked file from the message channel.
    16. Handles various exceptions and error cases during the process.
    """
    channel = bot.get_channel(channel_id)
    if channel is None:
        colorlog.error(f"Channel with ID {channel_id} not found.")
        log.error(f"Channel with ID {channel_id} not found.")
        return

    async for message in channel.history(limit=LIMIT):
        if message.author.name == WEBHOOK_USERNAME:
            for attachment in message.attachments:
                if attachment.filename.endswith(".pcap"):
                    if any(reaction.emoji == "👍" for reaction in message.reactions):
                        colorlog.info("Seen reaction found. Skipping download.")
                        log.info("Seen reaction found. Skipping download.")
                        continue  # Skip this message if the Seen reaction is present
                    name = attachment.filename
                    await download_pcap_file(attachment.url, name)
                    colorlog.info(f"Downloaded {name} from {attachment.url}")
                    log.info(f"Downloaded {name} from {attachment.url}")

                    try:
                        colorlog.info("Attempting to crack pcap files...")
                        log.info("Attempting to crack pcap files...")
                        try:
                            try:
                                await message.clear_reactions()
                                colorlog.info(
                                    f"Cleared all reactions from message ID {message.id}"
                                )
                                log.info(
                                    f"Cleared all reactions from message ID {message.id}"
                                )
                            except Exception as e:
                                colorlog.error(
                                    f"Failed to clear reactions from message ID {message.id}: {e}"
                                )
                                log.error(
                                    f"Failed to clear reactions from message ID {message.id}: {e}"
                                )

                            if platform.system() != "Linux":
                                colorlog.error(
                                    f"Windows is not supported for cracking. Please use Linux."
                                )
                                log.error(
                                    f"Windows attempted to be used for cracking. Failed"
                                )
                                # Wrong OS
                                await message.add_reaction("⛔")
                            else:
                                try:

                                    def crack(filename):
                                        """
                                        Attempts to crack a pcap file using various tools and techniques.

                                        Parameters:
                                        filename (str): The name of the pcap file to crack.

                                        Returns:
                                        bool: True if the cracking process is successful, False otherwise.
                                        """
                                        try:
                                            if os.geteuid() != 0:
                                                colorlog.critical(
                                                    "Please run this python script as root..."
                                                )
                                                log.critical("Root Running Failed...")
                                                return False

                                            if os.path.exists(filename) == 0:
                                                colorlog.critical(
                                                    f"File {filename} was not found, did you spell it correctly?"
                                                )
                                                log.critical(
                                                    f"File {filename} was not found"
                                                )
                                                return False

                                            checklist = [
                                                "airmon-ng",
                                                "tshark",
                                                "editcap",
                                                "pcapfix",
                                            ]
                                            installed = True

                                            for check in checklist:
                                                cmd = (
                                                    "locate -i "
                                                    + check
                                                    + " > /dev/null"
                                                )
                                                checked = os.system(cmd)
                                                if checked != 0:
                                                    colorlog.warning(
                                                        f"Could not find {check} in the system..."
                                                    )
                                                    log.warning(
                                                        f"Could not find {check} in the system..."
                                                    )
                                                    installed = False

                                            if not installed:
                                                colorlog.critical(
                                                    "Install those missing dependencies before you begin..."
                                                )
                                                return False

                                            new_filetype = filename[:-2]
                                            typetest = filename[-6:]

                                            colorlog.debug("Filename: " + filename)
                                            colorlog.debug("File Format: " + typetest)

                                            if typetest == "pcapng":
                                                colorlog.info(
                                                    "Crack Status: Converting file format..."
                                                )
                                                log.info("Converting pcapng file...")
                                                os.system(
                                                    "editcap -F pcap '"
                                                    + filename
                                                    + "' '"
                                                    + new_filetype
                                                    + "' > /dev/null"
                                                )
                                                filename = filename[:-2]
                                                colorlog.debug(
                                                    "New Filename: " + filename
                                                )

                                            os.system(
                                                "pcapfix -d '"
                                                + filename
                                                + "' -o Fixerror.pcap > /dev/null"
                                            )

                                            if os.path.isfile("./Fixerror.pcap") != 0:
                                                os.rename(filename, "Oldpcapfile.pcap")
                                                os.rename("Fixerror.pcap", filename)
                                                colorlog.info(
                                                    f"Crack Status: Fixing file errors for {filename}.."
                                                )
                                                log.info(
                                                    f"Fixing file errors for {filename}..."
                                                )
                                                colorlog.debug(
                                                    "Original Renamed: Oldpcapfile.pcap"
                                                )

                                            print("-" * 100)
                                            cmd = (
                                                "tcpdump -ennr '"
                                                + filename
                                                + "' '(type mgt subtype beacon)' | awk '{print $13}' | sed 's/[()]//g;s/......//' | sort | uniq > SSID.txt"
                                            )
                                            os.system(cmd)
                                            print("-" * 100)

                                            ssid = open("SSID.txt").readline().rstrip()
                                            os.remove("./SSID.txt")
                                            ssid = "00:" + ssid

                                            if ssid == "00:":
                                                colorlog.critical(
                                                    f"Empty SSID: The ssid {ssid} was given, This is not allowed..."
                                                )
                                                log.critical(
                                                    f"Empty SSID: The ssid [{ssid}] was found empty as '00:'."
                                                )
                                                return False
                                            else:
                                                colorlog.info(f"Service Set Id: {ssid}")
                                                log.info(f"Service Set Id Obtained")

                                            os.system(
                                                "aircrack-ng -b "
                                                + ssid
                                                + " '"
                                                + filename
                                                + "' > Answer.txt"
                                            )
                                            os.system(
                                                "awk '/KEY FOUND!/{print $(NF-1)}' Answer.txt > WepKey.txt"
                                            )
                                            os.remove("./Answer.txt")
                                            wep = open("WepKey.txt").readline().rstrip()
                                            os.remove("./WepKey.txt")
                                            colorlog.info("Wired Privacy Key : " + wep)
                                            log.info("Wired Privacy Key Obtained")

                                            os.system(
                                                "airdecap-ng -w "
                                                + wep
                                                + " '"
                                                + filename
                                                + "' "
                                                + "> /dev/null"
                                            )
                                            filename2 = filename[:-5]
                                            filename2 += "-dec.pcap"

                                            # Create the CRACKED directory if it doesn't exist
                                            if not os.path.exists("CRACKED"):
                                                os.makedirs("CRACKED")

                                            shutil.move(
                                                filename2, f"CRACKED/{filename2}"
                                            )

                                            # Rename the file within the CRACKED directory to include the SSID
                                            new_filename = f"Cracked_{ssid}.pcap"
                                            try:
                                                os.rename(
                                                    f"CRACKED/{filename2}",
                                                    f"CRACKED/{new_filename}",
                                                )
                                                colorlog.info(
                                                    f"Renamed Cracked File: {new_filename}"
                                                )
                                            except FileExistsError:
                                                os.remove(f"CRACKED/{new_filename}")
                                                os.rename(
                                                    f"CRACKED/{filename2}",
                                                    f"CRACKED/{new_filename}",
                                                )
                                                colorlog.info(
                                                    f"Renamed Cracked File: {new_filename}"
                                                )
                                            log.info("Cracked File Renamed")
                                            return True
                                        except Exception as e:
                                            colorlog.error(e)
                                            log.error(str(e))
                                            return False

                                    crack_test = crack(name)
                                    if crack_test:
                                        colorlog.info(
                                            f"Crack Status: Successfully cracked {name}"
                                        )
                                        log.info(
                                            f"Crack Status: Successfully cracked {name}"
                                        )
                                        # Cracking succeeded
                                        await message.add_reaction("👍")
                                        await upload_and_delete_files(message)
                                    elif not crack_test:
                                        colorlog.error(
                                            f"Crack Status: Failed to crack {name}"
                                        )
                                        log.error(
                                            f"Crack Status: Failed to crack {name}"
                                        )
                                        # Cracking has failed due to an error in the cracker function
                                        await message.add_reaction("👎")
                                    else:
                                        colorlog.critical("Non Boolean value returned")
                                        log.error("Non Boolean value returned")
                                        # Cracking failed due to value error returned from function
                                        await message.add_reaction("❔")

                                except Exception as e:
                                    colorlog.error(
                                        f"Failed to crack the pcap files...: {e}"
                                    )
                                    log.error(f"Failed to crack the pcap files...: {e}")
                                    # Cracking has failed due to an error from interpreter.
                                    await message.add_reaction("❌")
                        except discord.HTTPException as e:
                            colorlog.critical(f"A discord exception occurred: {e}")
                            log.critical(f"Discord exception occurred: {e}")
                            # Error Occurred, cracking was asked, Related to Discord HTTP exceptions.
                            await message.add_reaction("🚫")
                        except Exception as e:
                            colorlog.critical(f"Unexpected issue occurred: {e}")
                            log.critical(f"Unexpected issue occurred: {e}")
                            # Error Occurred, cracking was asked.
                            await message.add_reaction("⚠️")
                    except Exception as e:
                        colorlog.critical(f"Unexpected issue occurred: {e}")
                        log.critical(f"Unexpected issue occurred: {e}")
                        # Unknown Error Occurred, cracking was asked.
                        await message.add_reaction("⁉️")


async def upload_and_delete_files(message):
    """
    Uploads all files in the CRACKED directory as replies to the original message and then deletes them.

    Args:
        message (discord.Message): The original message that triggered the download.
    """
    # Ensure the CRACKED directory exists
    if not os.path.exists("CRACKED"):
        colorlog.warning("CRACKED directory does not exist?")
        log.warning("CRACKED directory does not exist?")
        return False

    # List all files in the CRACKED directory
    files_in_cracked = os.listdir("CRACKED")

    # Iterate over each file in the CRACKED directory
    for file_name in files_in_cracked:
        # Construct the full path to the file
        file_path = os.path.join("CRACKED", file_name)

        # Open the file in binary mode and read its content into a BytesIO object
        with open(file_path, "rb") as file:
            file_content = BytesIO(file.read())

            # Upload the BytesIO object as a file in a reply to the original message
            await message.channel.send(
                files=[discord.File(file_content, file_name)], reference=message
            )

            # Delete the file after uploading
            os.remove(file_path)

    # After uploading and deleting all files, remove the CRACKED directory itself
    shutil.rmtree("CRACKED")
    colorlog.info(
        "All files in the 'CRACKED' directory have been uploaded and deleted."
    )
    log.info("All files in the 'CRACKED' directory have been uploaded and deleted.")
    return True


async def download_pcap_file(url, filename):
    """
    Downloads a pcap file from the given URL and saves it to the specified filename.

    Args:
        url (str): The URL of the pcap file to download.
        filename (str): The filename to save the pcap file as.

    Returns:
        None
    """
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)


bot.run(TOKEN, log_handler=None)
