import json
import os
import requests
from pathlib import Path


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
    except FileNotFoundError:
        print("config.json not found.")
        exit(1)


# Step 2 & 3: Search for .pcap files and send them to Discord
def send_pcap_files_to_discord(webhook_url):
    # Ensure the path includes the current directory
    path = Path('.').resolve()

    # Debug print: Starting the search for .pcap files
    print("Starting search for .pcap files...")

    # Search for .pcap files
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.pcap'):
                file_path = os.path.join(root, file)
                print(f"Found .pcap file: {file_path}")

                # Debug print: Attempting to send the .pcap file to Discord
                print(f"Attempting to send {file_path} to Discord...")

                # Step 4: Send the .pcap file to Discord
                with open(file_path, 'rb') as f:
                    content = f.read()
                    # Adjusted to use 'files' parameter directly without specifying 'Content-Type'
                    response = requests.post(
                        webhook_url,
                        files={'file': ('file.pcap', content)}
                    )

                    # Debug print: Response status code
                    print(f"Response status code: {response.status_code}")

                    if response.status_code == 204:
                        print(f"Successfully sent {file_path} to Discord.")
                    else:
                        print(f"Failed to send {file_path} to Discord. Status Code: {response.status_code} {response.text}")
