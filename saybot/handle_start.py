from saybot import Update,ContextTypes,logging,Bot,os

# Define function to handle the /start command
async def handle_start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # Set up Telegram bot
    bot = Bot(token=os.getenv("API_BOT"))
    message = update.message
    user_full_name = f"{message.chat.first_name} {message.chat.last_name}"
    logging.info(f"/start command pressed by {user_full_name}")
    welcome_text = f"Hello {user_full_name}\nI'm \"SayChatGPT\" \nYour AI-powered chatbot \nI'm here to assist you. \nAsk your question.!"
    logging.info(welcome_text)
    await bot.send_message(chat_id=message.chat_id, text=welcome_text)
 