import os
import sys
import re
import shutil
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER')

def list_directory_contents(path, main_output_folder):
    """
    Lists all the contents of a directory and writes them to a text file in the main output folder.
    Args:
        path: Path to the directory to be listed.
        main_output_folder: Main folder for all output including the contents file.
    Returns:
        The path to the text file containing the directory contents.
    """
    try:
        if not os.path.exists(path):
            raise FileNotFoundError("File not found")
        contents = os.listdir(path)
        if contents:
            contents_file_path = os.path.join(main_output_folder, 'folder_contents.txt')
            with open(contents_file_path, 'w') as file:
                for item in contents:
                    file.write(f"{item}\n")
            return contents_file_path
        else:
            print("The directory is empty.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except PermissionError:
        print(f"Permission denied: Unable to access contents of '{path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def group_similar_filenames(contents_file_path, original_path, main_output_folder):
    """
    Groups similar filenames based on a specified pattern, and prepares them for copying.
    Args:
        contents_file_path: Path to the file containing the listed directory contents.
        original_path: Path to the original directory where files are stored.
        main_output_folder: Main folder for all output including grouped folders.
    Returns:
        A dictionary of groups with their respective file lists.
    """
    groups = defaultdict(list)
    pattern = r"(?:deviantart_)?\d+_([^.]+)"

    with open(contents_file_path, 'r') as file:
        file_names = file.readlines()

    for file_name in file_names:
        file_name = file_name.strip()
        match = re.search(pattern, file_name)
        if match:
            descriptor = match.group(1).strip().lower()
            descriptor = re.sub(r'[_\-\d()]+', ' ', descriptor).strip()
            descriptor = re.sub(r'\s+', ' ', descriptor)
            descriptor = re.sub(r'[^a-z0-9 ]', '', descriptor)
            groups[descriptor].append(file_name)
        else:
            groups['misc'].append(file_name)

    move_files_to_folders(groups, original_path, main_output_folder)
    return groups

def move_files_to_folders(groups, original_path, main_output_folder):
    """
    Copies files into their respective group folders within the main output folder.
    Args:
        groups: Dictionary of file groups.
        original_path: Path where the original files are stored.
        main_output_folder: Main folder where the group folders are created.
    """
    for descriptor, files in groups.items():
        if len(files) == 1:
            descriptor = 'misc'
        folder_path = os.path.join(main_output_folder, descriptor)
        os.makedirs(folder_path, exist_ok=True)
        for file_name in files:
            shutil.copy(os.path.join(original_path, file_name), os.path.join(folder_path, file_name))

def print_summary_of_folders(main_output_folder):
    """
    Prints a summary of folders and the number of files they contain within the main output folder.
    Args:
        main_output_folder: The main folder containing all output.
    """
    print("Folders created and file counts:")
    for folder_name in os.listdir(main_output_folder):
        folder_path = os.path.join(main_output_folder, folder_name)
        if os.path.isdir(folder_path):  # Ensure only directories are counted
            count = len(os.listdir(folder_path))
            print(f"Folder: {folder_name}, Files: {count}")

# Main execution block
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python script.py <folder_path>")
    folder_path = sys.argv[1]
    main_output_folder = os.path.join(OUTPUT_FOLDER, "categorized_files")
    os.makedirs(main_output_folder, exist_ok=True)
    contents_file_path = list_directory_contents(folder_path, main_output_folder)
    if contents_file_path:
        groups = group_similar_filenames(contents_file_path, folder_path, main_output_folder)
        print_summary_of_folders(main_output_folder)
