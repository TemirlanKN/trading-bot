from telethon import TelegramClient, events
import requests
import json
import asyncio
import os
import sys
from requests.auth import HTTPBasicAuth
from datetime import datetime

# Import configuration
try:
    from config import *
except ImportError:
    print("❌ Error: config.py not found!")
    print("Please create config.py with your API credentials")
    sys.exit(1)

class SignalFilterBot:
    def __init__(self):
        self.client = TelegramClient('session_name', TELEGRAM_API_ID, TELEGRAM_API_HASH)
        self.setup_event_handlers()
        
    def setup_event_handlers(self):
        @self.client.on(events.NewMessage(chats=CHANNELS_TO_MONITOR))
        async def handler(event):
            await self.process_message(event)
    
    async def process_message(self, event):
        """Process incoming message and filter for trading signals"""
        original_msg = event.message.message
        channel_name = event.chat.title if hasattr(event.chat, 'title') else 'Unknown Channel'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n[{timestamp}] 📨 New message from {channel_name}")
        print(f"📝 Content: {original_msg[:100]}...")

        # Filter message with AI
        ai_response = await self.filter_with_ai(original_msg, channel_name)
        
        if ai_response and ai_response.upper() != "IGNORE":
            await self.send_notifications(ai_response, channel_name, timestamp)
        else:
            print("🚫 Message filtered out (not a valid signal)")
    
    async def filter_with_ai(self, message, channel_name):
        """Send message to OpenAI for filtering"""
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": OPENAI_MODEL,
                    "messages": [
                        {
                            "role": "system",
                            "content": '''
You are an expert trading signal filter. Extract only valid forex/crypto trading signals.

VALID SIGNAL CRITERIA:
- Must contain a trading pair (e.g., XAU/USD, EUR/USD, BTC/USD)
- Must have clear entry price
- Must have stop loss (SL)
- Must have at least one take profit (TP)
- Must specify action: BUY or SELL

If it's a valid signal, return in this format:
🚨 SIGNAL DETECTED 🚨

Pair: [trading pair]
Action: [BUY or SELL]
Entry: [entry price]
SL: [stop loss]
TPs: [list all TPs, e.g., TP1: xxx, TP2: xxx, ...]
Risk: [risk percentage if mentioned]

If the message is promotional, testimonial, invitation to paid groups, or doesn't contain clear trading parameters, return exactly: IGNORE

Examples:
- "Join our VIP group" → IGNORE
- "Great signals!" → IGNORE
- "BUY XAU/USD at 2330, SL 2325, TP1 2340, TP2 2350" → [SIGNAL] format
'''
                        },
                        {
                            "role": "user",
                            "content": f"Channel: {channel_name}\nMessage: {message}"
                        }
                    ],
                    "temperature": AI_TEMPERATURE
                },
                timeout=30
            )
            
            if response.status_code == 200:
                ai_reply = response.json()["choices"][0]["message"]["content"].strip()
                print(f"🤖 AI Response: {ai_reply}")
                return ai_reply
            else:
                print(f"❌ OpenAI API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("⏰ OpenAI API timeout")
            return None
        except Exception as e:
            print(f"❌ Error calling OpenAI: {str(e)}")
            return None
    
    async def send_notifications(self, signal_message, channel_name, timestamp):
        """Send filtered signal to Telegram and/or WhatsApp"""
        formatted_message = f"{signal_message}\n\n📊 Source: {channel_name}\n⏰ Time: {timestamp}"
        
        # Send to Telegram
        if SEND_TO_TELEGRAM:
            try:
                await self.client.send_message('me', formatted_message)
                print("✅ Signal sent to Telegram Saved Messages")
            except Exception as e:
                print(f"❌ Error sending to Telegram: {str(e)}")
        
        # Send to WhatsApp
        if SEND_TO_WHATSAPP:
            success = self.send_whatsapp_message(formatted_message)
            if success:
                print("✅ Signal sent to WhatsApp")
            else:
                print("❌ Failed to send to WhatsApp")
    
    def send_whatsapp_message(self, message):
        """Send message to WhatsApp via Twilio"""
        try:
            if TWILIO_ACCOUNT_SID == "YOUR_TWILIO_SID":
                print("📲 WhatsApp not configured - skipping")
                return False
                
            response = requests.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json",
                auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
                data={
                    "From": WHATSAPP_FROM_NUMBER,
                    "To": WHATSAPP_TO_NUMBER,
                    "Body": message
                },
                timeout=30
            )
            
            if response.status_code == 201:
                return True
            else:
                print(f"❌ Twilio Error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ WhatsApp Error: {str(e)}")
            return False
    
    async def start(self):
        """Start the bot"""
        await self.client.start()
        
        print("🤖 Signal Filter Bot Started!")
        print("=" * 50)
        print(f"📱 Monitoring {len(CHANNELS_TO_MONITOR)} channels:")
        for channel in CHANNELS_TO_MONITOR:
            print(f"   • {channel}")
        print(f"💬 Telegram notifications: {'✅ Enabled' if SEND_TO_TELEGRAM else '❌ Disabled'}")
        print(f"📲 WhatsApp notifications: {'✅ Enabled' if SEND_TO_WHATSAPP else '❌ Disabled'}")
        print("=" * 50)
        print("⏹️  Press Ctrl+C to stop")
        
        await self.client.run_until_disconnected()

    async def send_status_message(self, text):
        """Send a status message to Telegram and WhatsApp."""
        if SEND_TO_TELEGRAM:
            try:
                await self.client.send_message('me', text)
            except Exception as e:
                print(f"❌ Error sending status to Telegram: {str(e)}")
        if SEND_TO_WHATSAPP:
            self.send_whatsapp_message(text)

def send_to_n8n_webhook(signal_message):
    webhook_url = "https://ktim9908.app.n8n.cloud/webhook-test/01ccec63-5b71-4977-9159-9aefcccd9c7f"
    data = {"message": signal_message}
    try:
        r = requests.post(webhook_url, json=data)
        print(f"[n8n] Sent to webhook: {r.status_code}")
    except Exception as e:
        print(f"[n8n] Error sending to webhook: {e}")

async def main():
    bot = SignalFilterBot()
    try:
        await bot.client.start()
        await bot.send_status_message("🚦 Signal Filter Bot has started and is now monitoring your channels.")
        await bot.start()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
        await bot.send_status_message("🛑 Signal Filter Bot has been stopped by the user.")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        await bot.send_status_message(f"❌ Signal Filter Bot crashed with error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

send_to_n8n_webhook("🚨 Test signal from Telethon script!") 