
from saybot import Update,ContextTypes,logging,generate_response,emoji,\
    generate_chat,generate_image,store_user_data,check_prompt_balance,sqlite3,os

from saybot.config import ConfigClass

db_path = os.path.join(os.getcwd(),"database","user_data.db")


def choose_model(prompt): # method for chosing the Model as per user command
    config = ConfigClass()
    func = config.current_model_function()
    if func is not None:
        response = func(prompt=prompt)
        return response
    else:
        logging.error("Model does not exist")

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

                    ai_response = choose_model(message_text)
                    ## Adding Usage statistics
                    with sqlite3.connect(db_path) as connection:
                        cursor = connection.cursor()
                        cursor.execute("SELECT * FROM usage_analysis WHERE id=?",(update.message.from_user.id,))
                        data=cursor.fetchone()
                        prompt_balance = data[2]
                        prompt_quota = data[3]
                        connection.commit()
                    display_text = f"{ai_response}\n****Your Account****\nPrompt Balance:{prompt_balance}\nDaily Quota:{prompt_quota}"

                    logging.info(f"AI - {display_text}")
                    await update.message.reply_text(reply_to_message_id=update.message.id,text=display_text)
                    await store_user_data(update=update)  # Store user data in MySQL
                    
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