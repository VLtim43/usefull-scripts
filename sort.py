import os
import sys

def folder(path):
    try:
        # check if the folder path exists
        if not os.path.exists(path):
            raise FileNotFoundError("file not found")

        contents = os.listdir(path)
        if contents:
            print("content of the folder:")
            for item in contents:
                print(item)
            else:
                print(item)
        else:
            print("folder is empty")         
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except PermissionError:
        print(f"Permission denied: Unable to access contents of '{folder_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# use
if len(sys.argv) < 2:
    sys.exit(1)

folder_path = sys.argv[1]
folder(folder_path)
