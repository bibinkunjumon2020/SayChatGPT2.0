from saybot import Application,os,CommandHandler,MessageHandler,filters,handle_start_command,handle_message
 
if __name__ == '__main__':

    application = Application.builder().token(token=os.getenv("API_BOT")).build()
    application.add_handler(CommandHandler('start',handle_start_command))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_message))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND,handle_message))

    # Start the bot
    application.run_polling(1.0)
