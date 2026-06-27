from flask import Flask, request, jsonify
from openai import OpenAI
import os
import requests

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("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"))

TELEGRAM_BOT_TOKEN = os.getenv("d67a420ec78124c965e5f7b4b6c378c621f1710d3e04460d")
TELEGRAM_CHAT_ID = os.getenv("-1003738638265")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    return requests.post(url, json=payload, timeout=15)

def get_ai_analysis(signal_data):
    prompt = f"""
You are a crypto trading assistant.
Analyze this live alert in 4 short lines.

Symbol: {signal_data.get('symbol')}
Side: {signal_data.get('side')}
Entry: {signal_data.get('entry')}
Target: {signal_data.get('target')}
SL: {signal_data.get('sl')}
Price: {signal_data.get('price')}
Volume: {signal_data.get('volume')}
RSI: {signal_data.get('rsi')}
VWAP: {signal_data.get('vwap')}

Return:
1. Bias
2. Risk
3. Confirmation
4. One-line action note
"""
    response = client.responses.create(
        model="gpt-5.5",
        input=prompt
    )
    return response.output_text

@app.route("/alert-receive", methods=["POST"])
def alert_receive():
    data = request.get_json(force=True)

    ai_text = get_ai_analysis(data)

    message = f"""📢 Live Trade Alert

Symbol: {data.get('symbol')}
Side: {data.get('side')}
Entry: {data.get('entry')}
Target: {data.get('target')}
SL: {data.get('sl')}

AI Analysis:
{ai_text}
"""
    send_telegram(message)
    return jsonify({"status": "ok"}), 200
