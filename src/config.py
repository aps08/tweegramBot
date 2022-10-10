"""
All id, key and token for twitter and telegram.
"""
import os

# Your telegram API ID
TEL_API_ID = os.environ.get("TEL_API_ID")
# Your telegram API hash
TEL_API_HASH = os.environ.get("TEL_API_HASH")
# Telegram group name you want to read
TEL_GROUP = os.environ.get("TEL_GROUP")
# Twitter API key
TWT_API_KEY = os.environ.get("TWT_API_KEY")
# Twitter API secret
TWT_API_SECRET = os.environ.get("TWT_API_SECRET")
# Twitter access token
TWT_ACCESS_TOKEN = os.environ.get("TWT_ACCESS_TOKEN")
# Twitter access token secret
TWT_ACCESS_TOKEN_SECRET = os.environ.get("TWT_ACCESS_TOKEN_SECRET")
