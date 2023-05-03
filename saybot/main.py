from saybot import Application,os,CommandHandler,MessageHandler,filters,handle_start_command,handle_message,\
                    handle_command_gpt35turbo,handle_command_textdavinci003
 
if __name__ == '__main__':

    application = Application.builder().token(token=os.getenv("API_BOT")).build()
    
    application.add_handler(CommandHandler('start',handle_start_command))
    application.add_handler(CommandHandler('gpt35turbo',handle_command_gpt35turbo)) # Model gpt-3.5-turbo used
    application.add_handler(CommandHandler('textdavinci003',handle_command_textdavinci003))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_message))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND,handle_message))

    # Start the bot
    application.run_polling(1.0)
