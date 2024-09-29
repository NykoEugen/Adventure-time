import os

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
NGROK_TUNNEL_URL = os.getenv('NGROK_TUNNEL_URL')
DB_URL = os.getenv('DB_URL')
OPENAI_KEY = os.getenv('OPENAI_KEY')
