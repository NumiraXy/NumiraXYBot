# main.py
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from app import config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"👋 Hello {user.first_name}!\n\n"
        "Welcome to Numira XY Bot.\n"
        "Use the menu below to get started."
    )
    await update.message.reply_text(text)

def main():
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    logging.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
