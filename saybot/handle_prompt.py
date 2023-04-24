
from saybot import Update,ContextTypes,logging,generate_response,emoji,datetime,timedelta,generate_chat


promt_time_stamp = {} # dictionary for storing each users' last used time and count
user_promt_limit =10 # prompt limit for each user with in 24 hours

async def promt_limit(update:Update): # daily prompt limit is defined
    user_id = update.message.chat_id # individual user IDs
    now = datetime.now()   # current time

    if user_id in promt_time_stamp:
        last_sent = promt_time_stamp[user_id]['time']
        if (now-last_sent) < timedelta(hours=24) and promt_time_stamp[user_id]['count'] >= user_promt_limit: # checking 24 hr and usage count
            logging.info("Limit Crossed")
            return False
        elif(now-last_sent >= timedelta(hours=24)): # If 24 hr crossed from last usage
            promt_time_stamp[user_id]={'time':now,'count':1}
            return True
        else:                                       # Increase usage count till 'user_promt_limit'
            promt_time_stamp[user_id]['count'] += 1 
            return True
    else:
        promt_time_stamp[user_id]={'time':now,'count':1}
        return True


async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE): # handle the user promts
    logging.info("inside chat messages")
    prompt_permission = await promt_limit(update=update) # Users daily limit checking(True or False )
    logging.info(promt_time_stamp)
    if prompt_permission:
        if update.message.text: #checking the input is text(emoji also a text)
            message_text = update.message.text
            try:
                list_of_emojis = emoji.emoji_list(message_text) # listing emojis in user input to avoid processing
                if isinstance(message_text,str) and len(list_of_emojis) == 0:
                    logging.info(f"User - \n {message_text}")
                    # ai_response = generate_response(message_text) # return is  never None
                    ai_response = generate_chat(message_text) # return is  never None

                    logging.info(f"AI - {ai_response}")
                    await update.message.reply_text(reply_to_message_id=update.message.id,text=ai_response)
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
        await update.message.reply_text(reply_to_message_id=update.message.id,text="Limit Crossed")