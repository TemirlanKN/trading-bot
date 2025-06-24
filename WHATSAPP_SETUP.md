# WhatsApp Integration Setup Guide

## Step 1: Create Twilio Account

1. Go to https://www.twilio.com/try-twilio
2. Sign up for a free account
3. Verify your email and phone number

## Step 2: Get Twilio Credentials

1. Go to https://console.twilio.com/
2. Copy your **Account SID** (starts with AC...)
3. Copy your **Auth Token** (click "show" to reveal)
4. Replace in `signal_filter.py`:
   ```python
   twilio_sid = "AC1234567890abcdef..."  # Your Account SID
   twilio_auth_token = "1234567890abcdef..."  # Your Auth Token
   ```

## Step 3: Set Up WhatsApp Sandbox

1. Go to https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. Click "Send a WhatsApp message"
3. You'll see the sandbox number: `+14155238886`
4. Send the provided code to that number via WhatsApp
5. You'll receive a confirmation message

## Step 4: Configure Your WhatsApp Number

1. In `signal_filter.py`, replace:
   ```python
   whatsapp_to_number = "whatsapp:+1234567890"  # Replace with your actual number
   ```
2. Format: `whatsapp:+[country code][phone number]`
   - Example: `whatsapp:+1234567890` (US number)
   - Example: `whatsapp:+447123456789` (UK number)

## Step 5: Test WhatsApp Integration

1. Run your script: `python signal_filter.py`
2. Wait for a signal from your monitored channels
3. You should receive the signal on both Telegram and WhatsApp

## Troubleshooting

- **"Not authorized" error**: Make sure you sent the code to the sandbox number
- **"Invalid phone number"**: Check the format (must include country code)
- **No messages received**: Verify your Twilio account has credits (free tier includes some)

## Production Setup (Optional)

For production use, you can:

1. Upgrade to a paid Twilio account
2. Get a dedicated WhatsApp Business number
3. Replace the sandbox number with your business number

## Cost Information

- **Free tier**: 1,000 messages/month
- **Paid tier**: ~$0.0075 per message
- **WhatsApp Business**: Additional setup required
