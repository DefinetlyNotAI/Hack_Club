import os
import sys

# Get current username
try:
    username = os.environ.get("USERNAME")
except Exception as e:
    print(f"An error occured fetching your username: {e}")
    exit(e)

# Construct path
path = f"C:\\Users\\{username}\\AppData\\Local\\JetBrains\\Installations\\dotPeek242\\dotPeek64.exe"

if sys.argv[1] is None:
    print("You need to include the dll path AFTER typing `python open.dll.py`")
    exit("No file parsed")
elif not sys.argv[1].endswith(".dll")
    print("The path MUST lead to a `.dll` file, the file path given does not!")
    print(sys.argv[1])
    exit("Non DLL file parsed")

try:
    # Check if path exists
    if os.path.exists(path):
        # Get DLL path from command line arguments
        dll_path = sys.argv[1]
    
        # Construct full command
        command = f'"{path}" "{dll_path}"'
    
        # Execute command
        os.system(command)
    else:
        print(f"dotPeek does not exist: {path}")
        print("Please make sure you have it installed in that directory")
        exit("dotPeek does not exist")
except Exception as e:
    print(f"An error occured executing the script dotPeek64: {e}")
    exit(e)
