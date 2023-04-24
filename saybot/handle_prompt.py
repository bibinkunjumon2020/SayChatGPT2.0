from saybot import Update,ContextTypes,logging,generate_response,emoji

async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE):
    logging.info("inside chat messages")
    if update.message.text:
        message_text = update.message.text
        try:
            list_of_emojis = emoji.emoji_list(message_text) # listing emojis in user input to avoid processing
            
            if isinstance(message_text,str) and len(list_of_emojis) == 0:
                logging.info(f"User - \n {message_text}")
                ai_response = generate_response(message_text) # return is  never None
                logging.info(f"AI - {ai_response}")
                await update.message.reply_text(reply_to_message_id=update.message.id,text=ai_response)
            else:
                logging.error(str(list_of_emojis))
                await update.message.reply_text(reply_to_message_id=update.message.id,text="Only Text Input Permitted")
            
        except Exception as e:
            logging.error(f"An error occurred while processing user input: {e}")
            await update.message.reply_text(reply_to_message_id=update.message.id, text="Sorry, an error occurred while processing your message.")
    else:
        logging.error("Input is not a [update.message.text] or is a [update.message.media]")
        await update.message.reply_text(reply_to_message_id=update.message.id,text="Only Text Input Permitted")