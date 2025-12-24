from flask import Flask, request, jsonify
import google.generativeai as genai
import requests, os, json
from collections import defaultdict
from datetime import datetime
import logging

app = Flask(__name__)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# WhatsApp Cloud API - YOUR VALUES
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "825417140654819")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "gemini-bot-2025")
META_API_URL = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"

# Gemini Pro
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')
conversations = defaultdict(list)

def send_whatsapp_reply(to_phone, message):
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": message[:1000]}
    }
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    try:
        response = requests.post(META_API_URL, json=payload, headers=headers)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Send error: {e}")
        return False

def get_gemini_reply(phone, user_message):
    conv = conversations[phone]
    system_prompt = """You are a professional customer support assistant. 
Answer concisely (under 800 chars), professionally, and helpfully. 
Use bullet points when listing options."""
    
    conv.append({"role": "user", "parts": [user_message]})
    history = conv[-8:]  # Last 8 exchanges
    full_prompt = [{"role": "user", "parts": [system_prompt]}] + history
    
    try:
        response = model.generate_content(full_prompt)
        reply = response.text
        conv.append({"role": "model", "parts": [reply]})
        return reply
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        return "Thanks for your message! Our team will respond soon."

@app.route("/whatsapp-webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("Webhook verified")
        return challenge, 200
    return "Forbidden", 403

@app.route("/whatsapp-webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        logger.info(f"Webhook received: {data}")
        
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        
        if "messages" in value:
            message = value["messages"][0]
            from_phone = message["from"]
            text_body = message["text"]["body"]
            
            logger.info(f"Message from {from_phone}: {text_body}")
            
            reply = get_gemini_reply(from_phone, text_body)
            success = send_whatsapp_reply(from_phone, reply)
            
            logger.info(f"Reply sent to {from_phone}: {success}")
            
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    
    return jsonify({"status": "ok"}), 200

@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "WhatsApp + Gemini Bot LIVE",
        "phone_id": PHONE_NUMBER_ID,
        "webhook_url": f"https://YOUR-DOMAIN.onrender.com/whatsapp-webhook",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    logger.info(f"🚀 Bot starting for Phone ID: {PHONE_NUMBER_ID}")
    app.run(host="0.0.0.0", port=10000, debug=False)
