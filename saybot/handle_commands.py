from saybot import Update,ContextTypes,logging,Bot,os,store_user_data
from saybot.config import ConfigClass


# Define function to handle the /start command
async def handle_start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    bot = Bot(token=os.getenv("API_BOT"))   # Set up Telegram bot
    message = update.message
    user_full_name = f"{message.chat.first_name} {message.chat.last_name}"
    logging.info(f"/start command pressed by {user_full_name}")
    welcome_text = f"Hello {user_full_name}\nI'm \"SayChatGPT\" \nYour AI-powered chatbot \nI'm here to assist you. \nAsk your question.!\n"
    await bot.send_message(chat_id=message.chat_id, text=welcome_text)
    await store_user_data(update=update) # storing user credentials in DB
 
# Define function to handle the /gpt35turbo command
async def handle_command_gpt35turbo(update:Update,context:ContextTypes.DEFAULT_TYPE):
    bot = Bot(token=os.getenv("API_BOT"))   # Set up Telegram bot
    message = update.message
    ConfigClass.set_model_selection_command("gpt-3.5-turbo")  # set the new model selection command in the instance
    model_selection_command = ConfigClass.get_model_selection_command()  
    await bot.send_message(chat_id=message.chat_id, text="Model gpt-3.5-turbo selected for Conversation!!!")
    logging.info("***Inside handle_command_gpt35turbo ***" + str(model_selection_command))

# Define function to handle the /textdavinci003 command
async def handle_command_textdavinci003(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = Bot(token=os.getenv("API_BOT"))   # Set up Telegram bot
    message = update.message
    ConfigClass.set_model_selection_command("text-davinci-003")  # set the new model selection command in the instance
    model_selection_command = ConfigClass.get_model_selection_command() 
    await bot.send_message(chat_id=message.chat_id, text="Model text-davinci-003 selected for Conversation!!!") 
    logging.info("***Inside handle_command_textdavinci003***" + str(model_selection_command))
