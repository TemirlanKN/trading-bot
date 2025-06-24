# Telegram Trading Signal Filter Bot (Cloud + n8n)

This guide will help you set up, deploy, and run your trading signal filter bot on a cloud server (e.g., DigitalOcean), using environment variables for secrets, and integrating with n8n for notifications.

---

## Features

- Monitors multiple Telegram channels as a user (not a bot)
- Filters messages using OpenAI (ChatGPT)
- Forwards valid signals to WhatsApp (via Twilio), Telegram, or n8n
- Runs 24/7 on a cloud server (no need to keep your laptop on)

---

## 1. Prerequisites

- Telegram account (user, not bot)
- [OpenAI API key](https://platform.openai.com/api-keys)
- [Twilio account](https://www.twilio.com/) (for WhatsApp, optional)
- [DigitalOcean account](https://www.digitalocean.com/) or any VPS provider
- [n8n account](https://n8n.cloud/) (for workflow automation)

---

## 2. Cloud Server Setup (DigitalOcean Example)

### a. Create a Droplet

- Choose Ubuntu 22.04 LTS, cheapest plan is enough
- Set a root password (check your email)

### b. Connect via SSH

```bash
ssh root@YOUR_SERVER_IP
```

- Use the password from your email (change it on first login)

### c. Update and Install Dependencies

```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip git screen
```

---

## 3. Project Setup

### a. Upload Your Code

- **Option 1:** Use GitHub (recommended)
  ```bash
  git clone https://github.com/yourusername/yourrepo.git
  cd yourrepo
  ```
- **Option 2:** Use SCP from your laptop:
  ```bash
  scp -r /path/to/your/project root@YOUR_SERVER_IP:/root/
  cd trading-bot
  ```

### b. Create `.env` File (Do NOT commit this to GitHub!)

```bash
nano .env
```

Paste and fill in:

```
TELEGRAM_API_ID=your_id
TELEGRAM_API_HASH=your_hash
OPENAI_API_KEY=sk-...
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
WHATSAPP_TO_NUMBER=whatsapp:+1234567890
WHATSAPP_FROM_NUMBER=whatsapp:+14155238886
CHANNELS_TO_MONITOR=FX_TRADING_01,Daytrading_GOLD,...
OPENAI_MODEL=gpt-3.5-turbo
AI_TEMPERATURE=0.1
SEND_TO_TELEGRAM=True
SEND_TO_WHATSAPP=True
```

### c. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

---

## 4. Running the Bot

### a. Start the Bot

```bash
python3 signal_filter_enhanced.py
```

- On first run, log in with your Telegram phone number and code.

### b. Keep It Running 24/7

```bash
screen -S tradingbot
python3 signal_filter_enhanced.py
```

- Detach: `Ctrl+A` then `D`
- Reattach: `screen -r tradingbot`

---

## 5. n8n Integration (Webhook)

- In n8n, create a Webhook node (POST method)
- Copy the webhook URL
- In your Python script, use the `send_to_n8n_webhook()` function to POST signals to n8n
- Add WhatsApp, Telegram, Email, or other nodes in n8n to forward the signal

---

## 6. Best Practices

- **Never commit `.env` or secrets to GitHub**
- Add `.env`, `config_local.py`, `__pycache__/`, and `*.pyc` to `.gitignore`
- Use `python-dotenv` to load secrets from `.env`
- Use a cloud server for 24/7 operation
- Use n8n for flexible notifications and integrations

---

## 7. Troubleshooting

- **Bot not running?** Check for errors in the terminal
- **No messages sent?** Check your `.env` values and n8n webhook
- **Push blocked by GitHub?** Remove all secrets from your repo and history
- **Session file not found?** Log in with your Telegram account on first run
- **WhatsApp not working?** Check Twilio credentials and sandbox setup

---

## 8. Updating or Restarting

- To update code: Pull from GitHub or upload new files
- To restart: Re-run the `python3 signal_filter_enhanced.py` command (in `screen` if needed)
- To change channels or settings: Edit `.env` and restart the bot

---

## 9. Security Notes

- Keep your `.env` file safe and never share it
- Do not share your session file (`session_name.session`)
- Use strong passwords for your server

---

## 10. Example `.env` File

```
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_api_hash
OPENAI_API_KEY=sk-...
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
WHATSAPP_TO_NUMBER=whatsapp:+1234567890
WHATSAPP_FROM_NUMBER=whatsapp:+14155238886
CHANNELS_TO_MONITOR=FX_TRADING_01,Daytrading_GOLD
OPENAI_MODEL=gpt-3.5-turbo
AI_TEMPERATURE=0.1
SEND_TO_TELEGRAM=True
SEND_TO_WHATSAPP=True
```

---

## 11. Example `.gitignore`

```
.env
config_local.py
__pycache__/
*.pyc
```

---

## 12. Support

- If you get stuck, check the console output for errors
- Double-check your `.env` and credentials
- Ask for help with deployment, n8n, or Python if needed

---

**You are now ready to run your trading signal filter bot in the cloud, fully automated!** 🚀
