import os
from dotenv import load_dotenv
import sys

load_dotenv()
output_folder = os.getenv('OUTPUT_FOLDER')


def folder(path):
    try:
        # check if the folder path exists
        if not os.path.exists(path):
            raise FileNotFoundError("file not found")

        contents = os.listdir(path)
        if contents:
            new_output_folder = os.path.join(output_folder, "test")
            
            os.makedirs(new_output_folder, exist_ok=True)
            
            output_file_path = os.path.join(new_output_folder, 'folder_contents.txt')
            
            with open(output_file_path, 'w') as f:
                for item in contents:
                    f.write(f"{item}\n")
            print(f"Contents written to {output_file_path}")
        else:
            print("The folder is empty.")
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
