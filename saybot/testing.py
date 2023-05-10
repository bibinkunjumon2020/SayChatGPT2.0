import telegram


from telegram.ext import Updater, CommandHandler

# Define the command handler for the '/start' command
def start(update, context):
    # Send typing action to show the user that the bot is typing
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    # Simulate some processing time
    import time
    time.sleep(2)
    
    # Send the actual response
    update.message.reply_text('Hello, I am a bot!')

# Create an instance of the Updater class and add the command handler
API_BOT="6184007244:AAFYzjJ7TLbyImiy0qdRqA8zi6ZlawSxeO8"
updater = Updater(token=API_BOT, use_context=True, update_queue=None)

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))

# Start the bot
updater.start_polling()
