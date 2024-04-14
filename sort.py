import os
import sys
import re
import shutil
import json
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the output folder path from environment variables
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER')

def list_directory_contents(path):
    """ Lists the contents of the specified directory (files only) and writes them to a JSON file within a sorted folder. """
    if not os.path.exists(path):
        raise FileNotFoundError("File not found")
    
    contents = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    if contents:
        sort_files_folder = os.path.join(OUTPUT_FOLDER, "sorted_files")
        os.makedirs(sort_files_folder, exist_ok=True)
        contents_file_path = os.path.join(sort_files_folder, 'folder_contents.json')

        with open(contents_file_path, 'w') as file:
            json.dump(contents, file, indent=4)
        
        print(f"Contents written to {contents_file_path}")
        return contents_file_path
    else:
        print("The directory is empty.")

def group_similar_filenames(contents_file_path):
    """ Groups similar filenames based on a pattern and returns the groups, ignoring subdirectories. """
    groups = defaultdict(list)
    pattern = r"(?:deviantart_)?\d+_([^.]+)"
    with open(contents_file_path, 'r') as file:
        file_names = json.load(file)
    
    for file_name in file_names:
        match = re.search(pattern, file_name)
        if match:
            descriptor = re.sub(r'[_\-\d]+', ' ', match.group(1).lower()).strip()
            descriptor = re.sub(r'\s+', ' ', descriptor)
            groups[descriptor].append(file_name)
        else:
            groups['misc'].append(file_name)

    # Consolidate groups with only one file into 'misc'
    single_file_groups = [desc for desc, files in groups.items() if len(files) == 1]
    for desc in single_file_groups:
        if desc != 'misc':
            groups['misc'].extend(groups.pop(desc))

    return groups

def copy_files_to_folders(groups, original_path):
    """ Copies files to folders based on their groups within the output folder. """
    for descriptor, files in groups.items():
        folder_path = os.path.join(OUTPUT_FOLDER, descriptor)
        os.makedirs(folder_path, exist_ok=True)
        for file_name in files:
            shutil.copy2(os.path.join(original_path, file_name), os.path.join(folder_path, file_name))



if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python script.py <folder_path>")
    
    folder_path = sys.argv[1]
    try:
        contents_file_path = list_directory_contents(folder_path)
        if contents_file_path:
            groups = group_similar_filenames(contents_file_path)
            copy_files_to_folders(groups, folder_path)
    except Exception as e:
        print(f"An error occurred: {e}")
