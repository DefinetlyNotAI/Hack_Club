import shutil
from pathlib import Path


def copy_logs_to_same_dir():
    # Determine the directory of the current script
    script_dir = Path(__file__).resolve().parent

    # Define the source path
    source_path = Path(r"C:\Windows\System32\winevt\Logs")

    # Define the destination path as a subdirectory named 'LogBackup' in the script's directory
    destination_path = script_dir / "LogBackup"

    try:
        # Ensure the destination directory exists
        if not destination_path.exists():
            destination_path.mkdir(parents=True, exist_ok=True)

        # Iterate through each file in the source directory
        for file_path in source_path.glob("*.evtx"):
            # Extract just the filename from the full path
            file_name = file_path.name
            source_file = file_path
            destination_file = destination_path / file_name

            # Remove the destination file if it already exists
            if destination_file.exists():
                print(f"Overwriting {file_name} in the destination.")
                destination_file.unlink(
                    missing_ok=True
                )  # Safely remove the file if it exists

            # Copy the file to the destination directory
            shutil.copy(source_file, destination_file)
            print(f"Copied {file_name} to {destination_file}")

    except PermissionError:
        print("Permission denied. Please run the script as an administrator.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Call the function to copy the logs
copy_logs_to_same_dir()
