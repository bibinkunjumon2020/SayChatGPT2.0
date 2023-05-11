from saybot import Update,ContextTypes,logging,Bot,os,store_user_data,Any,\
            retrieve_user_file_table,CallbackContext,retrieve_chosen_file,ChatAction,InlineKeyboardButton,\
            InlineKeyboardMarkup
from saybot.config import ConfigClass
from saybot.select_file_config import SelectFileClass
# from telegram import InlineKeyboardButton,InlineKeyboardMarkup
# Create an alias for the default context type hint
Context = ContextTypes.DEFAULT_TYPE
file_id_list ={} # dictionary storing key-file name value-file_id
async def inline_button_click_handler(update:Update,context:CallbackContext):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
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
    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
    bot, message, user_full_name = get_message_data(update)
    logging.info(f"/start command pressed by {user_full_name}")
    welcome_text = f"Hello {user_full_name}\nI'm \"SayChatGPT\" \nYour AI-powered chatbot \nI'm here to assist you. \nAsk your question.!\n"
    await bot.send_message(chat_id=message.chat_id, text=welcome_text)
    await store_user_data(update=update) # storing user credentials in DB

# -- /elite command

async def handle_elite_command(update: Update, context: Context) -> None:
    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
    bot, message, user_full_name = get_message_data(update)
    elite_info = f'👋 Hello {user_full_name},\n'\
            f'We regret to inform you that the Membership Plans have not yet been initiated.'\
         f' However, we encourage you to stay tuned for future updates and announcements regarding the launch of our Membership Plans.'\
             f' We appreciate your patience and understanding.'\
             f'👍👍👍'
    await bot.send_message(chat_id=message.chat_id, text=elite_info)

 # -- /info command --
async def handle_info_command(update: Update, context: Context) -> None:
    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
    bot, message,_ = get_message_data(update)
    logging.info(f"/info command pressed")
    info_text = f'Introducing our Telegram bot, powered by OpenAI\'s ChatGPT and advanced image generation.' \
                f'Engage in dynamic conversations, receive insightful answers, and explore the endless possibilities of image generation.' \
                f'\nUpload files, collaborate effortlessly, and revolutionize your messaging experience.' \
                f'Elevate your conversations, unleash your creativity, and discover the future of intelligent chatbots.\n'\
                f'\nThis bot Operation description:\n\n'\
                f'/chatgpt 💬- This set the chat settings for text generation using ChatGPT.\n'\
                    f'You can type the questions in chat area,you will get answers till 2021 provided by OpenAI. '\
                     f'\nThis is the most powerful conversation LLM.\n\n' \
                f'/davincigpt 💬- This set the chat settings for text generation using  GPT3-Davinci model.'\
                f'You can type the questions in chat area,you will get answers till 2021 provided by OpenAI.\n\n'\
                f'/image 🧚- Thi set the chat settings for image generation using OpenAI\'s DALL.E2 model.'\
                       f' You can type your concept in chat settings.It will generate image.This model is littile bit slow.'\
                        f'So you may need to wait bit longer.And the image generated will purely depend on your prompt quality.\n\n'\
                f'/askyourbook 🙋- This is the most exciting feature of our bot.You can ask questions to any of your document\
                    or book.Type your questions in chat area.Our bot will generate answers from your book.\n\n'\
                f'/selectfile 🗃- You can select a file from your list of books to get answered.Once selected,you can start your interaction.\n\n'\
                f'/uploadfile 📤- You can upload file in pdf format.Size should be less than 10 MB(for trial members) for each file.\
                    And only one file upload at a time for trial members.\n\n'\
                f'/elite 🎊- This command helps you to join with the elite Club:👨‍🚀👨‍🚀👨‍🚀\n\nBenefits:🎁\n\n'\
                    f' 1. Multiple files(books) upload at once.\n'\
                    f' 2. No limit on number of books you can store for learning.\n'\
                    f' 3. File size could be more than 10 MB (file size = Telegram permitted).\n'\
                    f' 4. Faster response of image generation with liberal limits.\n'\
                    f' 5. Faster and better response of Text using ChatGPT.\n'\
                    f' 6. GPT-4 in future.\n'\
                    f' 7. Using Your own OpenAI API-Key : So that all limits based on your account with OpenAI.\n\n'\
                f'/start - This command just welcomes you to the bot.'

    await bot.send_message(chat_id=message.chat_id, text=info_text) 


#####     <-- OTHER COMMANDS -->
async def handle_model_selection_command(update: Update, context, model_command: Any) -> None:
    bot, message, _ = get_message_data(update)
    ConfigClass.set_model_selection_command(model_command)  # set the new model selection command in the instance
    model_selection_command = ConfigClass.get_model_selection_command()
    check_select_file = SelectFileClass.get_select_file_id()
    display_texts = {
        "uploadfile": "Upload your File for Chat.Only one PDF document at a time.(Max size = 10 MB) \n",
        "selectfile": "Your Files:📁\n",
        "dall.e2": f"👍 DALL·E 2 of OpenAI can create realistic images and art from a description.Input 'prompt'\
                    \n\nEx: walking banana",
        "askyourbook": "Your File is ready to answer.Start chat.. \nEx: summarise / give a title",
        "chatgpt":"👍 ChatGPT of OpenAI selected for your 💬 Input 'prompt'\n\nEx: explain gravity",
        "davincigpt":"👍 Davinci:GPT-3 of OpenAI selected for your 💬 Input 'prompt'\n\nEx: explain gravity",
        "selectcommand":"Choose a proper command",
    }
    
    display_text = display_texts.get(model_command, f"Model \"{model_command}\" selected for further TEXT generation!\
                                                    \nInput your 'prompt' for text response.\n\nEx: explain gravity")
    
    if model_command == "selectfile":
        reply_markup = define_options_inline_keyboard(update.message.from_user.id)
        if not reply_markup.inline_keyboard: #checking any is it empty / any files uploaded exist
            display_text = "No Files..! Please Upload Files to proceed"
        await bot.send_message(chat_id=message.chat_id, text=display_text, reply_markup=reply_markup)
    elif model_command == "askyourbook":
        if check_select_file is None:
            display_text = "You must select a file for interaction"
        await bot.send_message(chat_id=message.chat_id, text=display_text)
    else:
        await bot.send_message(chat_id=message.chat_id, text=display_text)
    
    logging.info(f"***Inside handle_command_{model_command} ***{model_selection_command}")

# Define function to handle the /chatgpt command
async def handle_command_chatgpt(update: Update, context: Context) -> None:
    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
    await handle_model_selection_command(update, context, "chatgpt")

# Define function to handle the /davincigpt command
async def handle_command_davincigpt(update: Update, context: Context) -> None:
    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
    await handle_model_selection_command(update, context, "davincigpt") 

# Define function to handle the /image command
async def handle_command_image_dalle2(update: Update, context: Context) -> None:
    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
    await handle_model_selection_command(update, context, "dall.e2") 

# Define function to handle the /uploadfile command
async def handle_command_upload_file(update: Update, context: Context) -> None:
    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
    if update.message.chat.type == 'private': #checking the message came from private chat with the bot
        await handle_model_selection_command(update, context, "uploadfile") 
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="This Feature is only for Individual use.")

# Define function to handle the /askyourbook command
async def handle_command_askyourbook(update: Update, context: Context) -> None:
    # await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
    # await handle_model_selection_command(update, context, "askyourbook") 
    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
    if update.message.chat.type == 'private': #checking the message came from private chat with the bot
        await handle_model_selection_command(update, context, "askyourbook") 
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="This Feature is only for Individual use.")


# Define function to handle the /askyourbook command
async def handle_command_select_file(update: Update, context: Context) -> None:
    # await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
    # await handle_model_selection_command(update, context, "selectfile") 
    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
    if update.message.chat.type == 'private': #checking the message came from private chat with the bot
        await handle_model_selection_command(update, context, "selectfile") 
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="This Feature is only for Individual use.")


# Define function to handle the /selectcommand command
async def handle_command_select_command(update: Update, context: Context) -> None:
    # await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
    # await handle_model_selection_command(update, context, "selectfile") 
    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
    await handle_model_selection_command(update, context, "selectcommand") 


    