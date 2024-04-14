import os
import sys
import json
import shutil
import re
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the output folder path from environment variables
output_base_path = os.getenv('OUTPUTH_PATH')
if not output_base_path:
    raise ValueError("The OUTPUTH_PATH environment variable is not set.")

output_folder_base = os.path.join(output_base_path, "Sorted folders")
os.makedirs(output_folder_base, exist_ok=True)

def list_directory_contents(input_folder_path):
    """Lists the contents of the specified directory (files only), and writes them to a JSON file."""
    if not os.path.exists(input_folder_path):
        raise FileNotFoundError(f"The directory {input_folder_path} does not exist.")
    
    files = [file for file in os.listdir(input_folder_path) if os.path.isfile(os.path.join(input_folder_path, file))]
    contents_file_path = os.path.join(output_folder_base, os.path.basename(input_folder_path), 'folder_contents.json')
    os.makedirs(os.path.dirname(contents_file_path), exist_ok=True)
    with open(contents_file_path, 'w') as file:
        json.dump(files, file, indent=4)
    return contents_file_path

def group_similar_filenames(contents_file_path):
    """Groups similar filenames based on a regex pattern and returns the groups."""
    groups = defaultdict(list)
    pattern = r"(?:deviantart_)?\d+_([^.]+)"
    with open(contents_file_path, 'r') as file:
        file_names = json.load(file)
    
    for file_name in file_names:
        match = re.search(pattern, file_name)
        if match:
            descriptor = re.sub(r'[_\-\d]+', ' ', match.group(1).lower()).strip()
            descriptor = re.sub(r'\s+', ' ', descriptor)
            # Sanitize descriptor to remove non-alphanumeric characters
            sanitized_descriptor = re.sub(r'[^a-z0-9 ]', '', descriptor).strip().replace(' ', '_')
            groups[sanitized_descriptor].append(file_name)
        else:
            groups['misc'].append(file_name)

    single_file_groups = [desc for desc, files in groups.items() if len(files) == 1]
    for desc in single_file_groups:
        if desc != 'misc':
            groups['misc'].extend(groups.pop(desc))

    return groups

def copy_files_to_folders(groups, original_path):
    """Copies files into folders based on their groups within the output folder, avoiding overwrites."""
    sub_output_folder = os.path.join(output_folder_base, os.path.basename(original_path))
    for descriptor, files in groups.items():
        folder_path = os.path.join(sub_output_folder, descriptor)
        os.makedirs(folder_path, exist_ok=True)
        for file_name in files:
            destination_path = os.path.join(folder_path, file_name)
            if not os.path.exists(destination_path):  # Check if the file already exists
                shutil.copy2(os.path.join(original_path, file_name), destination_path)
            else:
                print(f"File {file_name} already exists in {folder_path}. Skipping.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python script.py <input_folder_path>")
    
    input_folder_path = sys.argv[1]
    try:
        contents_file_path = list_directory_contents(input_folder_path)
        groups = group_similar_filenames(contents_file_path)
        copy_files_to_folders(groups, input_folder_path)
    except Exception as e:
        print(f"An error occurred: {e}")
