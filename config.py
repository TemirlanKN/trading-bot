# Configuration file for Signal Filter Bot
# Copy this file to config_local.py and fill in your actual credentials

from dotenv import load_dotenv
import os

load_dotenv()

# Telegram API credentials (from https://my.telegram.org/apps)
TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID"))
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")

# OpenAI API key (from https://platform.openai.com/api-keys)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Twilio WhatsApp credentials (from https://console.twilio.com/)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_TO_NUMBER = os.getenv("WHATSAPP_TO_NUMBER")
WHATSAPP_FROM_NUMBER = os.getenv("WHATSAPP_FROM_NUMBER")

# Channels to monitor (usernames without @)
CHANNELS_TO_MONITOR = os.getenv("CHANNELS_TO_MONITOR").split(",")

# AI Model settings
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE"))

# Notification settings
SEND_TO_TELEGRAM = os.getenv("SEND_TO_TELEGRAM") == "True"
SEND_TO_WHATSAPP = os.getenv("SEND_TO_WHATSAPP") == "True" 