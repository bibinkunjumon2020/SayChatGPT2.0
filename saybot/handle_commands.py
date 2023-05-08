from saybot import Update,ContextTypes,logging,Bot,os,store_user_data,Any,\
            retrieve_user_file_table,CallbackContext,retrieve_chosen_file
from saybot.config import ConfigClass
from saybot.select_file_config import SelectFileClass
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
# Create an alias for the default context type hint
Context = ContextTypes.DEFAULT_TYPE
file_id_list ={} # dictionary storing key-file name value-file_id
import json
async def inline_button_click_handler(update:Update,context:CallbackContext):
    query = update.callback_query
    await query.answer(text="File Selected..!")
    selected_file_id = file_id_list[query.data]
    # Retrieve file data:
    data = retrieve_chosen_file(selected_file_id)
    # ConfigClass.set_select_file_id(selected_file_id)
    SelectFileClass.set_select_file_id(selected_file_id)
    ConfigClass.set_model_selection_command("askyourbook")
    if data is not None:
        display_text =  f'You have successfully selected your file 🔸{query.data}🔸\n\nNow you can start interaction with your file🧞‍♂️like\n'\
                        f'🟡Generate Summary\n🟢Suggest a title🧏‍♂️\n🔵Ask questions from file content 🙋‍♀️\n\n'\
                        f'🟧 Brief about your File🟧\n\n'\
                        f'File Name : {data[0]}\n\n'\
                        f'Uploaded on : {data[1]}\n\n'\
                        f'Title : {data[2]}\n\n'\
                        f'Summary : {data[3]}\n'
        await query.edit_message_text(text=display_text,parse_mode="Markdown")
    
   
def define_options_inline_keyboard(user_id):
    data = retrieve_user_file_table(userid=user_id)
    keyboard=[]
    for item in data:
        file_id_list[item[0]] = item[4]
        button = InlineKeyboardButton(text = item[0],callback_data=item[0])
        keyboard.append([button])

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

# Define function to initialize bot and get message object
def get_message_data(update: Update) -> tuple:
    TOKEN = os.getenv("API_BOT")
    bot = Bot(TOKEN)
    message = update.message
    user_full_name = f"{message.chat.first_name} {message.chat.last_name}"
    return bot, message, user_full_name

# Define function to handle the /start command   <-- START COMMAND-->
async def handle_start_command(update: Update, context: Context) -> None:
    bot, message, user_full_name = get_message_data(update)
    logging.info(f"/start command pressed by {user_full_name}")
    welcome_text = f"Hello {user_full_name}\nI'm \"SayChatGPT\" \nYour AI-powered chatbot \nI'm here to assist you. \nAsk your question.!\n"
    await bot.send_message(chat_id=message.chat_id, text=welcome_text)
    await store_user_data(update=update) # storing user credentials in DB
 
#####     <-- OTHER COMMANDS -->
async def handle_model_selection_command(update: Update, context, model_command: Any) -> None:
    bot, message, _ = get_message_data(update)
    ConfigClass.set_model_selection_command(model_command)  # set the new model selection command in the instance
    model_selection_command = ConfigClass.get_model_selection_command()
    
    display_texts = {
        "uploadfile": "Upload your File for asking questions\n",
        "selectfile": "Your Files:\n",
        "dall.e2": f"Model \"{model_command}\" of OpenAI used for IMAGE generation.\
                      \nInput your 'prompt' for image generation.\n\nEx: drone carrying banana",
        "askyourbook": "Your File is ready to answer.Start chat.. \nEx:summarise/give a title"
    }
    
    display_text = display_texts.get(model_command, f"Model \"{model_command}\" selected for further TEXT generation!\
                                                    \nInput your 'prompt' for text response.\n\nEx: explain gravity")
    
    if model_command == "selectfile":
        reply_markup = define_options_inline_keyboard(update.message.from_user.id)
        await bot.send_message(chat_id=message.chat_id, text=display_text, reply_markup=reply_markup)
    else:
        await bot.send_message(chat_id=message.chat_id, text=display_text)
    
    logging.info(f"***Inside handle_command_{model_command} ***{model_selection_command}")

# Define function to handle the /gpt35turbo command
async def handle_command_gpt35turbo(update: Update, context: Context) -> None:
    await handle_model_selection_command(update, context, "gpt-3.5-turbo")

# Define function to handle the /textdavinci003 command
async def handle_command_textdavinci003(update: Update, context: Context) -> None:
    await handle_model_selection_command(update, context, "text-davinci-003") 

# Define function to handle the /image command
async def handle_command_image_dalle2(update: Update, context: Context) -> None:
    await handle_model_selection_command(update, context, "dall.e2") 

# Define function to handle the /uploadfile command
async def handle_command_upload_file(update: Update, context: Context) -> None:
    await handle_model_selection_command(update, context, "uploadfile") 

# Define function to handle the /askyourbook command
async def handle_command_askyourbook(update: Update, context: Context) -> None:
    await handle_model_selection_command(update, context, "askyourbook") 

# Define function to handle the /askyourbook command
async def handle_command_select_file(update: Update, context: Context) -> None:
    await handle_model_selection_command(update, context, "selectfile") 

    