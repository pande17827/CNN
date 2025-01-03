import os
import random
import string
import subprocess
import time
import threading

def generate_random_text_files(directory, file_name_length, interval):
    """
    Generate text files with random names, where the content matches the file name, and push the changes to a Git repository.
    Files will be deleted after 30 minutes.

    Parameters:
        directory (str): Folder in the current directory where files will be created.
        file_name_length (int): Length of the random file names (without extension).
        interval (int): Time interval (in seconds) between generating and pushing files.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    while True:
        # Generate a random file name
        file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=file_name_length))
        file_path = os.path.join(directory, f"{file_name}.txt")

        # Write the file name as the content
        with open(file_path, 'w') as file:
            file.write(file_name)

        print(f"File created: {file_path}")

        # Schedule file deletion after 30 minutes
        threading.Timer(1800, delete_file, args=(file_path,)).start()

        # Push the new file to the repository
        push_changes()

        # Wait before generating the next file
        time.sleep(interval)

def delete_file(file_path):
    """Delete the specified file."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File deleted: {file_path}")
    except Exception as e:
        print(f"An error occurred while deleting file {file_path}: {e}")

def push_changes():
    """Stage, commit, and push changes to the Git repository."""
    try:
        # Stage all files
        subprocess.run(["git", "add", "-A"], check=True)

        # Commit the changes
        commit_message = "Added new file"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push the changes
        subprocess.run(["git", "push"], check=True)

        print("Changes successfully pushed to the repository!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during git operations: {e}")

# Configuration
output_directory = "random_text_files"  # Folder in the current directory
file_name_length = 8                      # Length of the random file names
interval = 10                             # Time interval between generating and pushing files (in seconds)

# Generate files
generate_random_text_files(output_directory, file_name_length, interval)