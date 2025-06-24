# Telegram Trading Signal Filter Bot

🤖 An intelligent bot that monitors Telegram trading channels, filters messages using AI, and forwards only valid trading signals to your Telegram and WhatsApp.

## Features

- 📱 **Multi-channel monitoring**: Monitor multiple Telegram channels simultaneously
- 🤖 **AI-powered filtering**: Uses OpenAI GPT to identify valid trading signals
- 💬 **Telegram notifications**: Sends filtered signals to your Telegram Saved Messages
- 📲 **WhatsApp integration**: Forward signals to WhatsApp via Twilio
- 🚫 **Smart filtering**: Ignores promotional messages, testimonials, and non-signal content
- ⏰ **Real-time processing**: Processes messages as they arrive

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `config.py` with your credentials:

```python
# Telegram API (from https://my.telegram.org/apps)
TELEGRAM_API_ID = 12345678
TELEGRAM_API_HASH = 'your_api_hash_here'

# OpenAI API (from https://platform.openai.com/api-keys)
OPENAI_API_KEY = "sk-your-openai-key-here"

# Channels to monitor
CHANNELS_TO_MONITOR = [
    'FX_TRADING_01',
    'your_channel_username'
]
```

### 3. Run the Bot

```bash
python signal_filter_enhanced.py
```

On first run, you'll be prompted to:

- Enter your phone number
- Enter the verification code sent to Telegram
- Enter your 2FA password (if enabled)

## WhatsApp Setup (Optional)

Follow the detailed guide in `WHATSAPP_SETUP.md`:

1. Create a Twilio account
2. Get your Account SID and Auth Token
3. Set up WhatsApp sandbox
4. Update `config.py` with Twilio credentials
5. Set `SEND_TO_WHATSAPP = True`

## How It Works

1. **Message Detection**: Bot monitors specified Telegram channels
2. **AI Analysis**: Each message is sent to OpenAI for analysis
3. **Signal Filtering**: AI determines if the message contains a valid trading signal
4. **Notification**: Valid signals are formatted and sent to you

### Valid Signal Criteria

- ✅ Contains trading pair (XAU/USD, EUR/USD, etc.)
- ✅ Has clear entry price
- ✅ Includes stop loss (SL) and take profit (TP)
- ✅ Actionable trading advice

### Filtered Out

- ❌ Promotional messages
- ❌ Customer testimonials
- ❌ Invitations to paid groups
- ❌ General comments without trading data

## Example Output

**Input Message:**

```
🚨 NEW SIGNAL 🚨
BUY XAU/USD at 2330.00
SL: 2325.00
TP: 2345.00
Risk: 2%
```

**Bot Output:**

```
🚨 SIGNAL DETECTED 🚨

Pair: XAU/USD
Entry: 2330.00
SL: 2325.00
TP: 2345.00
Risk: 2%

📊 Source: FX_TRADING_01
⏰ Time: 2024-01-15 14:30:25
```

## Configuration Options

### Channels

Add or remove channels in `config.py`:

```python
CHANNELS_TO_MONITOR = [
    'channel1',
    'channel2',
    'channel3'
]
```

### AI Settings

Adjust AI behavior:

```python
OPENAI_MODEL = "gpt-3.5-turbo"  # or "gpt-4"
AI_TEMPERATURE = 0.1  # Lower = more consistent
```

### Notifications

Enable/disable notification methods:

```python
SEND_TO_TELEGRAM = True
SEND_TO_WHATSAPP = False  # Set to True after Twilio setup
```

## Troubleshooting

### Common Issues

**"Session file not found"**

- Run the script and complete the login process

**"OpenAI API Error"**

- Check your API key in `config.py`
- Verify you have credits in your OpenAI account

**"WhatsApp not working"**

- Follow the Twilio setup guide
- Check your phone number format (must include country code)

**"Channel not found"**

- Make sure you're subscribed to the channel
- Check the channel username (without @ symbol)

### Logs

The bot provides detailed console output:

- 📨 Incoming messages
- 🤖 AI responses
- ✅ Successful notifications
- ❌ Errors and issues

## Security Notes

- Keep your API keys secure
- Don't share your `config.py` file
- The session file contains your login credentials
- Consider using environment variables for production

## Cost Information

- **Telegram**: Free
- **OpenAI**: ~$0.002 per 1K tokens (very cheap for this use case)
- **Twilio WhatsApp**: Free tier includes 1,000 messages/month

## Support

If you encounter issues:

1. Check the console output for error messages
2. Verify all API keys are correct
3. Ensure you're subscribed to the monitored channels
4. Check your internet connection

## License

This project is for educational purposes. Use responsibly and in compliance with Telegram's and OpenAI's terms of service.
