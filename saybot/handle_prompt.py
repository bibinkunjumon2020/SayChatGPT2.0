
from saybot import Update,ContextTypes,logging,generate_response,emoji,\
    generate_chat,generate_image,store_user_data,check_prompt_balance,sqlite3,os,validators,requests

from saybot.config import ConfigClass
from saybot.select_file_config import SelectFileClass
from saybot.generate_from_document import generate_response_from_userdoc


db_path = os.path.join(os.getcwd(),"database","user_data.db")


def choose_model(prompt,update:Update): # method for chosing the Model as per user command
    config = ConfigClass()
    func = config.current_model_function()
    if func is not None:
        if func == generate_response_from_userdoc:
            check_file_select = SelectFileClass.get_select_file_id()
            if check_file_select is None:
                response = "Choose your File for Interaction"
            else:
                response = func(prompt=prompt,update=update)
        else:
            response = func(prompt=prompt)
        return response         #it may return None if openai fails
    else:
        logging.error("Model does not exist")
        return "No Model" #model not in the dictionary Dont return None 
        

def check_response_url(response):
    if validators.url(response):
        return True #response is a url or image url
    else:
        return False # response is text

async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE): # handle the user promts
    prompt_permission = await check_prompt_balance(update=update) # Users daily limit checking(True or False )
   
    if prompt_permission:
        if update.message.text: #checking the input is text(emoji also a text)
            message_text = update.message.text
            try:
                list_of_emojis = emoji.emoji_list(message_text) # listing emojis in user input to avoid processing
                if isinstance(message_text,str) and len(list_of_emojis) == 0:
                    logging.info(f"User - \n {message_text}")
                    # ai_response = generate_response(message_text) # return is  never None
                    # ai_response = generate_chat(message_text) # return is  never None
                    # ai_response = generate_image(message_text) # return is  never None

                    ai_response = choose_model(message_text,update)
                    if ai_response != "No Model": # check the function dictionary returned wrong
                        ai_response_image_check = check_response_url(ai_response)  #checking response is image or not
                        if ai_response_image_check:
                            image_data = requests.get(ai_response).content
                            await context.bot.send_photo(chat_id=update.message.chat_id,photo=image_data)
                        else:
                            ## REDUCING PROMPT QUOTA Adding Usage statistics
                            with sqlite3.connect(db_path) as connection:
                                cursor = connection.cursor()
                                cursor.execute("SELECT * FROM usage_analysis WHERE id=?",(update.message.from_user.id,))
                                data=cursor.fetchone()
                                prompt_balance = data[2]
                                prompt_quota = data[3]
                                connection.commit()
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