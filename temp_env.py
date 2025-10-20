import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Smart Assistant Configuration
HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL")
HOME_ASSISTANT_TOKEN = os.getenv("HOME_ASSISTANT_TOKEN")
SMART_ASSISTANT_ENABLED = os.getenv("SMART_ASSISTANT_ENABLED", "false").lower() == "true"
