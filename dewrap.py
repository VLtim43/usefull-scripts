import os
import shutil
import sys

def dewrap(source_folder, file_extensions=None):
    """
    Consolidates image files from a source directory and its subdirectories into a single destination folder within the source directory.
    
    Args:
        source_folder (str): The directory to search for image files and also the destination for consolidated images.
        file_extensions (list): Optional. A list of file extensions to include (e.g., ['.jpg', '.png']). If None, defaults to common image formats.
    """
    destination_folder = os.path.join(source_folder, "Dewrapped images")
    if file_extensions is None:
        file_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']  # Add or remove extensions as needed.

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if any(file.lower().endswith(ext) for ext in file_extensions):
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_folder, file)

                # To prevent overwriting files with the same name, check if the destination file exists and rename if necessary.
                if os.path.exists(destination_path):
                    base, extension = os.path.splitext(file)
                    i = 1
                    new_file = f"{base}_{i}{extension}"
                    destination_path = os.path.join(destination_folder, new_file)
                    while os.path.exists(destination_path):
                        i += 1
                        new_file = f"{base}_{i}{extension}"
                        destination_path = os.path.join(destination_folder, new_file)

                shutil.copy(source_path, destination_path)  # Copy the file to the destination

    print("Images have been consolidated into:", destination_folder)

# Main execution block
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python script.py <source_folder>")
    source_folder = sys.argv[1]
    dewrap(source_folder)
