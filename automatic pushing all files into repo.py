import os
import subprocess
import time

# Define the repository path
repo_path = "/workspaces/CNN"  # Replace with your repo path
commit_message = "Auto-push: Updated all files"

# Change to the repository directory
os.chdir(repo_path)

def push_changes():
    try:
        # Stage all files
        subprocess.run(["git", "add", "."], check=True)

        # Commit the changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push the changes
        subprocess.run(["git", "push"], check=True)

        print("All files successfully pushed to the repository!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

# Run the push every minute
try:
    print("Auto-push started. Press Ctrl+C to stop.")
    while True:
        push_changes()
        time.sleep(30)  # Wait for 1 minute
except KeyboardInterrupt:
    print("Auto-push stopped.")
