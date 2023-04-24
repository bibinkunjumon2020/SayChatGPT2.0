# import openai
# import logging
# import os
# from dotenv import load_dotenv
# from pathlib import Path
# from telegram import Bot,Update,InputMediaPhoto
# from telegram.ext import Updater,CommandHandler,MessageHandler,filters,Application,ContextTypes
# import asyncio
# # Set base directory and load environment variables
# BASE_DIR = Path(__file__).resolve().parent.parent
# dotenv_path = os.path.join(BASE_DIR,".env")
# load_dotenv(dotenv_path)

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Set up OpenAI API key
# openai.api_key = os.getenv("API_OPENAI")
# # Set up Telegram bot
# bot = Bot(token=os.getenv("API_BOT"))

# def generate_response(message_text):
#     prompt = message_text+"?"
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=250,
#         n=1,
#         stop='.',
#         temperature=0.2,
#     )
#     message_response = response.choices[0].text + "."
#     return message_response

# Define function to handle incoming messages
# async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE):
#     logging.info("inside chat messages")
#     message_text = update.message.text
#     logging.info(f"User - \n {message_text}")
#     ai_response = generate_response(message_text)
#     logging.info(f"AI - {ai_response}")
#     await update.message.reply_text(reply_to_message_id=update.message.id,text=ai_response)

# # Define function to handle the /start command
# async def handle_start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
#     message = update.message
#     user_full_name = f"{message.chat.first_name} {message.chat.last_name}"
#     logging.info(f"/start command pressed by {user_full_name}")
#     welcome_text = f"Hello {user_full_name}\nI'm \"SayBotGPT\" \nYour AI-powered chatbot \nI'm here to assist you \nAsk your question.!"
#     logging.info(welcome_text)
#     await bot.send_message(chat_id=message.chat_id, text=welcome_text)


from saybot import Application,os,CommandHandler,MessageHandler,filters,handle_start_command,handle_message
 
if __name__ == '__main__':

    application = Application.builder().token(token=os.getenv("API_BOT")).build()
    application.add_handler(CommandHandler('start',handle_start_command))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_message))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND,handle_message))

    # Start the bot
    application.run_polling(1.0)
