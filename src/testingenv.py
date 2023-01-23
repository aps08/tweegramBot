import os

from dotenv import load_dotenv

load_dotenv()
print(os.environ.get("API_ID"))
print(os.environ.get("API_HASH"))
print(os.environ.get("API_KEY"))
print(os.environ.get("API_SECRET"))
print(os.environ.get("ACCESS_TOKEN"))
print(os.environ.get("ACCESS_TOKEN_SECRET"))
