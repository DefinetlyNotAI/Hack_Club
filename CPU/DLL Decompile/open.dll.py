import os
import sys

# Get current username
username = os.environ.get("USERNAME")

# Construct path
path = f"C:\\Users\\{username}\\AppData\\Local\\JetBrains\\Installations\\dotPeek242\\dotPeek64.exe"

# Check if path exists
if os.path.exists(path):
    # Get DLL path from command line arguments
    dll_path = sys.argv[1]

    # Construct full command
    command = f'"{path}" "{dll_path}"'

    # Execute command
    os.system(command)
else:
    print(f"Path does not exist: {path}")
