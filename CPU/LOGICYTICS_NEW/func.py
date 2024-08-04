# Add these imports at the top of your script
import datetime
import platform
import subprocess
import psutil
import wmi
from tqdm import tqdm
import os


def get_system_ram_info():
    svmem = psutil.virtual_memory()
    return f"Total RAM: {svmem.total / (1024 ** 3)} GB"


def get_system_software_info():
    return f"OS: {platform.system()} {platform.version()}"


def get_system_logs(source_path=r'C:/Windows/System32/winevt/Logs/System.evtx',
                    destination_path=os.path.join(os.getcwd(), 'SystemCopy.evtx')):
    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)

    # Open the source file in binary mode
    with open(source_path, 'rb') as src_file:
        # Calculate the size of the file to determine progress
        file_size = os.path.getsize(source_path)

        # Open the destination file in binary mode
        with open(destination_path, 'wb') as dst_file:
            # Use tqdm to create a progress bar
            progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, desc="Copying System Log")

            # Read and write the file in chunks
            chunk_size = 4096  # Size of chunks to read/write at a time
            while True:
                chunk = src_file.read(chunk_size)
                if not chunk:
                    break  # Exit loop if no more data to read
                dst_file.write(chunk)
                progress_bar.update(len(chunk))

            progress_bar.close()


def get_system_cpu_info():
    cpu_info = platform.processor()
    return f"CPU Info: {cpu_info}"


def get_system_gpu_info():
    # Placeholder function. For accurate GPU info, consider using specific tools or libraries.
    return "GPU Info: Not Available"


def get_system_tree_directory():
    return f"System Root Directory: {psutil.disk_partitions()[0].mountpoint}"


def get_system_age():
    today = datetime.date.today()
    try:
        bios_date_str = subprocess.check_output("wmic bios get serialnumber", shell=True).decode('utf-8').split(":")[
            1].strip()
        bios_date = datetime.datetime.strptime(bios_date_str, "%d/%m/%Y").date()
        return f"System Age: {(today - bios_date).days} days"
    except IndexError:
        return "System Age: Unable to determine."


def get_system_identifications():
    wmi_obj = wmi.WMI()
    computer_name = wmi_obj.Win32_ComputerSystem()[0].Name
    return f"Computer Name: {computer_name}"


def get_windows_data():
    try:
        # Define the PowerShell command as a string
        ps_command = 'Get-WmiObject -query "SELECT * FROM SoftwareLicensingService"'

        # Open PowerShell and execute the command
        output = subprocess.run(['powershell', '-Command', ps_command], capture_output=True, text=True)

        # Check if the command execution was successful
        if output.returncode == 0:
            # Return the output without any leading/trailing whitespace
            return output.stdout.strip()
        else:
            # If there was an error, return a message indicating failure
            return "Windows Key: Not Available; Error executing command."
    except Exception as e:
        # Handle any other exceptions that might occur
        return f"Windows Key: Not Available; {str(e)}"


def list_wifi_profiles():
    try:
        output = subprocess.check_output('netsh wlan show profiles', shell=True)
        return output.decode('utf-8')
    except Exception as e:
        return "Error listing Wi-Fi profiles: " + str(e)


def get_wifi_profile_details(profile_name):
    try:
        # First, check if the profile exists
        output = subprocess.check_output(f'netsh wlan show profile name="{profile_name}"', shell=True)
        if "does not exist" in output.decode('utf-8'):
            return f"Profile '{profile_name}' does not exist."

        # Then, retrieve the key=clear section
        output = subprocess.check_output(f'netsh wlan show profile name="{profile_name}" key=clear', shell=True)
        lines = output.decode('utf-8').split('\n')
        for line in lines:
            if "Key Content" in line:
                return line.split(":")[1].strip()  # Return the key content
        return "Key not found."
    except Exception as e:
        return "Error retrieving Wi-Fi profile details: " + str(e)


# Example usage
print(list_wifi_profiles())
for profile in ['YourWiFiProfileName1', 'YourWiFiProfileName2']:  # Replace with your actual profile names
    print(get_wifi_profile_details(profile))
print(get_system_ram_info())
print(get_system_software_info())
print(get_system_cpu_info())
print(get_system_gpu_info())
print(get_system_tree_directory())
print(get_system_age())
print(get_system_identifications())
print(get_windows_data())
get_system_logs()
