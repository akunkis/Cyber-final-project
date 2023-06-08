import os
import winshell
import shutil
import sys
import winreg



# Add Tesseract OCR directory to the system's PATH variable
def add_tesseract_to_path():
    # Specify the path to the Tesseract OCR directory
    tesseract_path = os.path.join(os.path.dirname(sys.argv[0]), r"Tess")

    # Open the system's Environment Variables registry key
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment', 0, winreg.KEY_ALL_ACCESS)

    # Get the current value of the PATH variable
    path_value = winreg.QueryValueEx(key, 'PATH')[0]

    # Split the PATH value into individual directories
    path_dirs = path_value.split(';')

    # Check if the Tesseract OCR directory is already present in the PATH
    if tesseract_path not in path_dirs:
        print("Making Path")

        # Append the Tesseract OCR directory to the PATH value
        updated_path = f'{path_value};{tesseract_path}'

        # Update the PATH variable with the new value
        winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, updated_path)

    else:
        print("Already exists")

    # Close the registry key
    winreg.CloseKey(key)


# Now the Tesseract OCR executable should be accessible from the system's PATH

# Rest of your code...


def create_startup_shortcut():
    Filepath = os.path.dirname(sys.argv[0])

    exe_path = os.path.join(Filepath, "main.exe") # Replace with the actual path to main.exe

    # Create a shortcut of the main.exe file
    shortcut_path = os.path.join(winshell.startup(), "MainShortcut.lnk")
    winshell.CreateShortcut(
        Path=shortcut_path,
        Target=exe_path,
        Description="Shortcut to Main",
        Icon=(exe_path, 0),
    )

    # Move the shortcut to the Startup folder
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    shutil.move(shortcut_path, os.path.join(startup_folder, "MainShortcut.lnk"))


# Call the function to create the startup shortcut
if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Set the script directory as the working directory
    os.chdir(script_dir)

    add_tesseract_to_path()
    create_startup_shortcut()
