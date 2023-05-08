from saybot import Application,os,CommandHandler,MessageHandler,filters,handle_start_command,handle_message,\
                    handle_command_gpt35turbo,handle_command_textdavinci003,handle_command_image_dalle2,\
                    handle_command_upload_file,Update,handle_command_askyourbook,handle_command_select_file,\
                    CallbackQueryHandler,inline_button_click_handler

from telegram.ext import CallbackContext
from saybot.file_upload import file_upload

# Define an error handler function
def error_handler(update: Update, context: CallbackContext):
    # Log the exception details
    print(f"Exception occurred: {context.error}")

    # You can also send a message to the user or perform any other necessary actions

if __name__ == '__main__':

    application = Application.builder().token(token=os.getenv("API_BOT")).build()
    
    application.add_error_handler(error_handler)

    application.add_handler(CommandHandler('start',handle_start_command))
    application.add_handler(CommandHandler('gpt35turbo',handle_command_gpt35turbo)) # Model gpt-3.5-turbo used
    application.add_handler(CommandHandler('textdavinci003',handle_command_textdavinci003))
    application.add_handler(CommandHandler('image',handle_command_image_dalle2))
    application.add_handler(CommandHandler('uploadfile',handle_command_upload_file))
    application.add_handler(CommandHandler('askyourbook',handle_command_askyourbook))
    application.add_handler(CommandHandler('selectfile',handle_command_select_file))
 
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_message))
    # application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND,handle_message))
    application.add_handler(MessageHandler(filters.Document.MimeType("application/pdf"),file_upload))


    application.add_handler(CallbackQueryHandler(inline_button_click_handler))

    # Start the bot
    application.run_polling(1.0)
