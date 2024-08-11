import psutil
import platform
import os
from tqdm import tqdm
import wmi
import subprocess


class SystemInfo:
    def __init__(self):
        self.source_path = r"C:/Windows/System32/winevt/Logs/System.evtx"
        self.destination_path = os.path.join(os.getcwd(), "SystemCopy.evtx")

    @staticmethod
    def ram():
        svmem = psutil.virtual_memory()
        return f"Total RAM: {svmem.total / (1024 ** 3)} GB"

    @staticmethod
    def software():
        return f"OS: {platform.system()} {platform.version()}"

    def system_logs(self):
        os.makedirs(os.path.dirname(self.destination_path), exist_ok=True)
        with open(self.source_path, "rb") as src_file, open(
            self.destination_path, "wb"
        ) as dst_file:
            file_size = os.path.getsize(self.source_path)
            progress_bar = tqdm(
                total=file_size, unit="B", unit_scale=True, desc="Copying System Log"
            )
            chunk_size = 4096
            while True:
                chunk = src_file.read(chunk_size)
                if not chunk:
                    break
                dst_file.write(chunk)
                progress_bar.update(len(chunk))
            progress_bar.close()

    @staticmethod
    def cpu():
        cpu_info = platform.processor()
        return f"CPU Info: {cpu_info}"

    @staticmethod
    def gpu():
        return "GPU Info: Not Available"

    @staticmethod
    def tree():
        return f"System Root Directory: {psutil.disk_partitions()[0].mountpoint}"

    @staticmethod
    def age():
        try:
            bios_date = (
                subprocess.check_output("wmic bios get serialnumber", shell=True)
                .decode("utf-8")
                .split(":")[1]
                .strip()
            )
            return f"System Age: {bios_date}"
        except IndexError:
            return "System Age: Unable to determine."

    @staticmethod
    def id():
        wmi_obj = wmi.WMI()
        computer_name = wmi_obj.Win32_ComputerSystem()[0].Name
        return f"Computer Name: {computer_name}"

    @staticmethod
    def win_data():
        try:
            ps_command = 'Get-WmiObject -query "SELECT * FROM SoftwareLicensingService"'
            output = subprocess.run(
                ["powershell", "-Command", ps_command], capture_output=True, text=True
            )
            if output.returncode == 0:
                return output.stdout.strip()
            else:
                return "Windows Key: Not Available; Error executing command."
        except Exception as e:
            return f"Windows Key: Not Available; {str(e)}"

    @staticmethod
    def __list_wifi_profiles():
        try:
            output = subprocess.check_output("netsh wlan show profiles", shell=True)
            lines = output.decode("utf-8").split("\n")
            profile_lines = [line for line in lines if "All User Profile" in line]
            profile_names = [line.split(":")[1].strip() for line in profile_lines]
            return profile_names
        except Exception as e:
            return "Error listing Wi-Fi profiles: " + str(e)

    @staticmethod
    def __get_wifi_profile_details(profile_name):
        try:
            escaped_profile_name = f'"{profile_name}"'
            output = subprocess.check_output(
                f"netsh wlan show profile name={escaped_profile_name} key=clear",
                shell=True,
            )
            try:
                lines = output.decode("latin-1").split("\n")
            except UnicodeDecodeError:
                lines = output.decode("utf-8").split("\n")
            for line in lines:
                if "Key Content" in line:
                    password_line = line.split(":")
                    if len(password_line) > 1:
                        password = password_line[1].strip()
                        return f"{profile_name}: {password}"
            return f"Password not found for '{profile_name}'."
        except Exception as e:
            return (
                f"Error retrieving Wi-Fi profile details for '{profile_name}': {str(e)}"
            )

    def wifi(self):
        profiles = self.__list_wifi_profiles()
        wifi = []
        if profiles:
            for profile in profiles:
                details = self.__get_wifi_profile_details(profile)
                wifi = details
            return wifi
        else:
            return "No WiFi profiles found."


# Main logic

sys_info = SystemInfo()
print(sys_info.wifi())
print(sys_info.ram())
print(sys_info.software())
print(sys_info.cpu())
print(sys_info.gpu())
print(sys_info.tree())
print(sys_info.age())
print(sys_info.id())
print(sys_info.win_data())
sys_info.system_logs()
