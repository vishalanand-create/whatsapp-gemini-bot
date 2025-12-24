# WhatsApp + Gemini Pro AI Bot

Automatic AI-powered customer support bot that integrates Google Gemini Pro with WhatsApp Business Cloud API. Receive customer messages on WhatsApp and auto-reply with intelligent AI responses.

## Features

✅ **WhatsApp Cloud API Integration** - Production-ready webhook
✅ **Google Gemini Pro** - Advanced AI responses with conversation memory
✅ **Free Tier Compatible** - Works with free Gemini API tier
✅ **Easy Deployment** - Deploy to Render (free tier)
✅ **Conversation Memory** - Maintains context for 8-message history per customer
✅ **Production Ready** - Logging, error handling, rate limiting

## Architecture

```
Customer (WhatsApp) → Meta Cloud API → Your Webhook → Gemini Pro → Auto Reply
```

## Prerequisites

- WhatsApp Business Cloud API access with credentials:
  - `PHONE_NUMBER_ID`
  - Permanent `ACCESS_TOKEN`
  - `VERIFY_TOKEN` (custom)
- Google Gemini API Key (free tier available)
- Render or similar hosting (free tier: 750 hrs/month)

## Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/whatsapp-gemini-bot
cd whatsapp-gemini-bot
cp .env.example .env
```

### 2. Configure `.env`

```env
PHONE_NUMBER_ID=825417140654819
ACCESS_TOKEN=your_permanent_token_here
VERIFY_TOKEN=gemini-bot-2025
GEMINI_API_KEY=your_gemini_key_here
```

### 3. Deploy to Render

1. Push to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect this repo
4. Set environment variables (from `.env`)
5. Deploy

### 4. Configure Meta Webhook

Meta Developers → WhatsApp → Configuration:
```
Webhook URL: https://your-render-app.onrender.com/whatsapp-webhook
Verify Token: gemini-bot-2025
Subscribe to: messages
```

## How It Works

1. Customer sends message → WhatsApp Cloud API → Your webhook
2. Flask app extracts message + phone number
3. Calls Gemini Pro with system prompt + conversation history
4. Sends reply back via WhatsApp Cloud API
5. Stores conversation memory (per phone number)

## File Structure

```
whatsapp-gemini-bot/
├── app.py              # Main Flask app
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

## Cost Breakdown

| Service | Free Tier | Cost (if over) |
|---------|-----------|----------------|
| Gemini API | 15 RPM, 1M tokens/day | ₹0.075/million tokens |
| WhatsApp | N/A | ₹0.30 inbound, ₹0.38 outbound |
| Render | 750 hrs/month | ~₹400/month for always-on |

**Total monthly cost for 100 conversations/day**: ~₹1000-1500

## Customization

### Change System Prompt

Edit in `app.py`:
```python
system_prompt = """Your custom instructions here..."""
```

### Add RAG/Knowledge Base

```python
def get_relevant_docs(query):
    # Implement vector search (Pinecone, etc.)
    return docs

# In get_gemini_reply:
relevant_docs = get_relevant_docs(user_message)
full_prompt = [system_prompt] + relevant_docs + history
```

### Database Support

For persistent storage beyond bot restart:
```python
import sqlite3
# Or use PostgreSQL on Render
```

## Testing

### Local Testing

```bash
pip install -r requirements.txt
export GEMINI_API_KEY=your_key
python app.py
# Open http://localhost:10000
```

### Webhook Verification

```bash
curl "http://localhost:10000/whatsapp-webhook?hub.mode=subscribe&hub.verify_token=gemini-bot-2025&hub.challenge=test"
```

## Production Checklist

- [ ] Permanent ACCESS_TOKEN created in Meta dashboard
- [ ] Webhook URL configured & verified in Meta
- [ ] Environment variables set in Render
- [ ] Gemini API key active & rate limits checked
- [ ] Render app deployed & running
- [ ] Test message flow end-to-end
- [ ] Monitor logs for errors
- [ ] Set up backup/failover if needed

## Troubleshooting

**Bot not replying:**
- Check Render logs: `https://dashboard.render.com`
- Verify ACCESS_TOKEN is permanent (not user-level)
- Test Gemini API key separately

**403 Webhook error:**
- Ensure VERIFY_TOKEN matches in Meta dashboard
- Check if token has special characters (escape in env vars)

**Rate limits:**
- Upgrade Gemini to paid tier for >15 RPM
- Implement request queuing with Redis

## Support

For WhatsApp Cloud API issues: [Meta Documentation](https://developers.facebook.com/docs/whatsapp/cloud-api/)
For Gemini issues: [Google AI Studio](https://ai.google.dev/)

## License

MIT

## Contributors

- Created for MyOperator team

---

**Made with ❤️ for customer success teams**
