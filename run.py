# parth7802
import os
import subprocess
import sys
import time
import psutil
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS credentials
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

if not AWS_ACCESS_KEY or not AWS_SECRET_KEY:
    print("Error: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in .env file.")
    sys.exit(1)

# Binary configuration
BINARY_NAME = "tracker"
BINARY_PATH = os.path.join(os.path.dirname(__file__), BINARY_NAME)

def is_binary_running():
    """Check if the tracker binary is running."""
    for proc in psutil.process_iter(['name', 'exe']):
        if proc.info['exe'] and os.path.basename(proc.info['exe']) == BINARY_NAME:
            return True
    return False

def start_binary():
    """Start the tracker binary if not running."""
    if not os.path.exists(BINARY_PATH):
        print(f"Error: Required binary '{BINARY_NAME}' missing. Download from GitHub Releases.")
        sys.exit(1)
    
    if not os.access(BINARY_PATH, os.X_OK):
        print(f"Error: Binary '{BINARY_NAME}' is not executable. Run: chmod +x {BINARY_NAME}")
        sys.exit(1)

    if not is_binary_running():
        try:
            cmd = [
                BINARY_PATH,
                f"--access-key={AWS_ACCESS_KEY}",
                f"--secret-key={AWS_SECRET_KEY}",
                f"--region={AWS_REGION}"
            ]
            subprocess.Popen(cmd, preexec_fn=os.setsid, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(2)
            if not is_binary_running():
                print(f"Error: Failed to start '{BINARY_NAME}'.")
                sys.exit(1)
        except Exception as e:
            print(f"Error starting binary: {e}")
            sys.exit(1)

# Check and start binary
start_binary()

# Run the original app.py
try:
    subprocess.run([sys.executable, "app.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running app.py: {e}")
    sys.exit(1)
