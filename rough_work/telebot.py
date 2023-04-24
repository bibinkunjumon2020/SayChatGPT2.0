"""
THis file is not used in this app work
"""

import openai

import logging
import os
from dotenv import load_dotenv
from pathlib import Path

from telegram import Bot,Update
from telegram.ext import Updater,CommandHandler,MessageHandler,filters,Application,ContextTypes


# # Set base directory and load environment variables
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# dotenv_path = os.path.join(BASE_DIR, ".env")
# load_dotenv(dotenv_path)

# Set base directory and load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR,".env")
load_dotenv(dotenv_path)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set up OpenAI API key
openai.api_key = os.getenv("API_OPENAI")

# Set up Telegram bot
bot = Bot(token=os.getenv("API_BOT"))

# Define function to generate response using ChatGPT
def generate_response(message_text):
    prompt = message_text+"?"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=250,
        n=1,
        stop='.',
        temperature=0.2,
    )
    message_response = response.choices[0].text + "."
    return message_response

# Define function to handle incoming messages
async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE):
    logging.info("inside chat messages")
    message_text = update.message.text
    logging.info(f"User - \n {message_text}")
    ai_response = generate_response(message_text)
    logging.info(f"AI - {ai_response}")
    # await bot.send_message(chat_id=message.chat_id, text=bot_response)
    await update.message.reply_text(ai_response)

# Define function to handle the /start command
async def handle_start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    message = update.message
    logging.info("/start command pressed")
    welcome_text = "Hello there !\nI'm \"SayBotGPT\" \nYour AI-powered chatbot \nI'm here to answer any questions \nLet's get started..!"
    logging.info(welcome_text)
    await bot.send_message(chat_id=message.chat_id, text=welcome_text)

# Create an instance of the updater and dispatcher
# updater = Updater(bot=bot, update_queue=None)
# dispatchers = updater.dispatcher
application = Application.builder().token(token=os.getenv("API_BOT")).build()

# Add handlers for the /start command and incoming messages
# dispatcher.add_handler(CommandHandler("start", handle_start_command))
# dispatcher.add_handler(MessageHandler(filters.Text, handle_message))

application.add_handler(CommandHandler('start',handle_start_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_message))

# Start the bot
# updater.start_polling()
application.run_polling(1.0)
