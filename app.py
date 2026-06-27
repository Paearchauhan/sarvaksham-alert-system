from flask import Flask, request
import requests

app = Flask(__name__)

# 🔑 Replace with your actual bot token & chat ID
TELEGRAM_BOT_TOKEN = '8879566560:AAG1hRQP8HRziipOvSwyMDKK4IFj-LOIv5Q'
TELEGRAM_CHAT_ID = '-1003738638265'

@app.route('/alert-receive', methods=['POST'])
def alert_receive():
    data = request.json
    message = f"""
📢 *Chartink Alert Received*

🔹 *Symbol*: {data.get('symbol')}
🔹 *Open*: {data.get('open')}
🔹 *High*: {data.get('high')}
🔹 *Low*: {data.get('low')}
🔹 *Close*: {data.get('close')}
🔹 *VWAP*: {data.get('vwap')}
🔹 *Volume*: {data.get('volume')}
🔹 *Stop Loss*: {data.get('sl')}
🔹 *Target*: {data.get('target')}
"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=payload)
    return '✅ Alert sent to Telegram', 200
