import winreg
import sys
def initial_setup():
      # Get the path of the Python script
      script_path = sys.argv[0]

      # Create a new key for the .sprite file extension
      with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ".sprite") as key:
      # Set the default value to the name of the file type
            winreg.SetValue(key, "", winreg.REG_SZ, "Sprite File")

      # Create a new key for the file type
      with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "SpriteFile") as type_key:
            # Set the default value to the name of the file type
            winreg.SetValue(type_key, "", winreg.REG_SZ, "Sprite File")

            # Create a new key for the shell command
            with winreg.CreateKey(type_key, "shell\\open\\command") as command_key:
                  # Set the default value to the command to run the Python script with the clicked file as an argument
                  winreg.SetValue(command_key, "", winreg.REG_SZ, f'"{sys.executable}" "{script_path}" "%1"')
