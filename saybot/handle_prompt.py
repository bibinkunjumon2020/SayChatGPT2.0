
from saybot import Update,ContextTypes,logging,emoji,\
    store_user_data,check_prompt_balance,sqlite3,os,validators,requests,ChatAction,generate_image
   

from saybot.config import ConfigClass
from saybot.select_file_config import SelectFileClass
from saybot.generate_from_document import generate_response_from_userdoc

from saybot.timeout_checker import check_api_request
db_path = os.path.join(os.getcwd(),"database","user_data.db")


async def choose_model(prompt,update:Update,context:ContextTypes.DEFAULT_TYPE): # method for chosing the Model as per user command
    config = ConfigClass()
    func = config.current_model_function()
    if func is not None:
        if func == generate_response_from_userdoc:
            check_file_select = SelectFileClass.get_select_file_id()
            if check_file_select is None:
                response = "Choose your File for Interaction"
            else:
                response = func(prompt=prompt,update=update)
        elif func == generate_image:
            # keyboard = [[InlineKeyboardButton("Processing...", callback_data='processing')]]
            # reply_markup = InlineKeyboardMarkup(keyboard)
            # message = await context.bot.send_message(chat_id=update.effective_chat.id, text='Please wait while I process your request...', reply_markup=reply_markup)
            message = await context.bot.send_message(chat_id=update.effective_chat.id, text='Please wait while I process your request...')
            # response = func(prompt=prompt)
            response = await check_api_request(func,prompt)
            # logging.info(response)
            message_id = message.message_id  # Retrieve the message ID
            await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=message_id,text='Processing complete!', reply_markup=None)

        else: #chatgpt,davinchichat
            # response = func(prompt=prompt)
            response = await check_api_request(func,prompt)
        return response         #it may return None if openai fails
    else:
        logging.error("Model does not exist")
        return "No Model" #model not in the dictionary Dont return None 
        

def decrement_chat_quota(update:Update):
    ## REDUCING PROMPT QUOTA Adding Usage statistics
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM usage_analysis WHERE id=?",(update.message.from_user.id,))
        data=cursor.fetchone()
        prompt_balance = data[2]
        prompt_quota = data[3]
        connection.commit()
        return prompt_balance,prompt_quota

def check_response_url(response): # determine the reponse is an image or text
    if validators.url(response):
        return True #response is a url or image url
    else:
        return False # response is text

async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE): # handle the user promts
    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING) #setting typing status
    prompt_permission = await check_prompt_balance(update=update) # Users daily limit checking(True or False )
   
    if prompt_permission:
        if update.message.text: #checking the input is text(emoji also a text)
            message_text = update.message.text
            try:
                list_of_emojis = emoji.emoji_list(message_text) # listing emojis in user input to avoid processing
                if isinstance(message_text,str) and len(list_of_emojis) == 0:
                    logging.info(f"User - \n {message_text}")
                    # await context.bot.send_message(chat_id=update.effective_chat.id,text='Please wait while I process your request...')
                    ai_response = await choose_model(prompt=message_text,update=update,context=context)
                    if ai_response == None:
                        await update.message.reply_text(reply_to_message_id=update.message.id,text="Sorry for inconvenience.Sever Load.Try later")
                        return
                    if ai_response != "No Model": # check the function dictionary returned None.
                        ai_response_image_check = check_response_url(ai_response)  #checking response is image or not
                        if ai_response_image_check: #If DALL.E2
                            # first i update user status
                            await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.UPLOAD_PHOTO)
                            image_data = requests.get(ai_response).content
                            await context.bot.send_photo(chat_id=update.message.chat_id,photo=image_data)
                            prompt_balance,prompt_quota =decrement_chat_quota(update)
                            await context.bot.send_message(chat_id=update.message.chat_id,text=f'Prompt Balance:{prompt_balance}\nDaily Quota:{prompt_quota}')
                        else:
                            prompt_balance,prompt_quota = decrement_chat_quota(update)
                            display_text = f"{ai_response}\n\n****Your Account****\n\nPrompt Balance:{prompt_balance}\nDaily Quota:{prompt_quota}"

                            # logging.info(f"AI - {display_text}")
                            await update.message.reply_text(reply_to_message_id=update.message.id,text=display_text) #parse mode MarkdownV2 gives error Can't parse entities:

                        await store_user_data(update=update)  # Store user data in MySQL
                    else:
                        await update.message.reply_text(reply_to_message_id=update.message.id,text="Please run a proper command before conversation !!!")
                else:
                    logging.error(str(list_of_emojis))
                    await update.message.reply_text(reply_to_message_id=update.message.id,text="Only Text Input Permitted")
                    
            except Exception as e:
                logging.error(f"An error occurred while processing user input: {e}")
                await update.message.reply_text(reply_to_message_id=update.message.id, text="Sorry, an error occurred while processing your message.")
            
        else: #input is media content
            logging.error("Input is not a [update.message.text] or is a [update.message.media]")
            await update.message.reply_text(reply_to_message_id=update.message.id,text="Only Text Input Permitted")
    else: # Daily limit over
        await update.message.reply_text(reply_to_message_id=update.message.id,text="Daily Limit Crossed \nUsed:10\nTotal:10")