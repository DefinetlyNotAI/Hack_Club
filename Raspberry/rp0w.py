import requests
import colorlog
import json
import os
import pwnagotchi.plugins as plugins
from pathlib import Path
from datetime import datetime

# Configure colorlog for logging messages with colors
logger = colorlog.getLogger()
logger.setLevel(colorlog.DEBUG)  # Set the log level to INFO to capture all relevant logs

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


log = Log(filename="Pwngotchi_Plugin_Errors.log", max_size=1000)


def activate_plugin():
    """
    Function called when the plugin is activated.
    It should contain the logic to integrate with pwngotchi.
    """
    webhook_url = read_webhook_url()
    send_pcap_files_to_discord(webhook_url)


# Step 1: Read the webhook URL from config.json
def read_webhook_url():
    try:
        with open('config.json', 'r') as file:
            data = json.load(file)
            return data['webhookUrl']
    except FileNotFoundError as e:
        colorlog.critical(f"Error reading config.json: {e}")
        log.critical(f"Error reading config.json: {e}")
        exit(1)


# Step 2 & 3: Search for .pcap files and send them to Discord
def send_pcap_files_to_discord(webhook_url):
    # Define the paths to search
    paths_to_search = [
        '.',  # Current Dir
        '/root/handshakes/'  # Specific directory for pwngotchi handshakes (pcap)
    ]

    # Debug print: Starting the search for .pcap files
    colorlog.info("Starting search for .pcap files and attempting to send them to Discord via webhook...")

    # Iterate over each path
    for path in paths_to_search:
        path = Path(path).resolve()  # Resolve the path to ensure it's absolute

        # Search for .pcap files in the current path
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.pcap'):
                    file_path = os.path.join(root, file)
                    colorlog.debug(f"Found .pcap file: {file_path}")

                    # Debug print: Attempting to send the .pcap file to Discord
                    colorlog.debug(f"Attempting to send {file_path} to Discord...")

                    # Step 4: Send the .pcap file to Discord
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        # Adjusted to use 'files' parameter directly without specifying 'Content-Type'
                        response = requests.post(
                            webhook_url,
                            files={'file': ('file.pcap', content)}
                        )

                        # Debug print: Response status code
                        colorlog.debug(f"Response status code: {response.status_code}")

                        if response.status_code == 204 or response.status_code == 200:
                            colorlog.info(f"Successfully sent {file_path} to Discord.")
                        else:
                            colorlog.error(f"Failed to send {file_path} to Discord. Status Code: {response.status_code}")
                            log.error(f"Failed to send {file_path} to Discord. Status Code: {response.status_code}")
                        colorlog.debug(f"Response text: {response.text}")
                        log.info("Returned from Discord: " + response.text)


activate_plugin()
