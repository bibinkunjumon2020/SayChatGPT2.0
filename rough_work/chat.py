"""
THis file is not used in this app work
"""


import openai
import telebot

import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Set base directory and load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR,".env")
load_dotenv(dotenv_path)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set up OpenAI API key
openai.api_key = os.getenv("API_OPENAI")

# Set up Telegram bot
bot = telebot.TeleBot(os.getenv("API_BOT"))

# Define function to generate response using ChatGPT
def generate_response(message_text):
    prompt = message_text
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop='.',
        temperature=0.5,
    )
    message_response = response.choices[0].text+"."
    return message_response

# Define function to handle incoming messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    logging.info("Bot started")
    message_text = message.text
    logging.info(f"User- {message_text}")
    bot_response = generate_response(message_text)
    logging.info(f"AI - {bot_response}")
    bot.reply_to(message, bot_response)

# Start bot
bot.polling()
