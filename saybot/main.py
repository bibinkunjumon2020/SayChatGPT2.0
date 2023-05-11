from saybot import Application,os,CommandHandler,MessageHandler,filters,handle_start_command,handle_message,\
                    handle_command_chatgpt,handle_command_davincigpt,handle_command_image_dalle2,\
                    handle_command_upload_file,Update,handle_command_askyourbook,handle_command_select_file,\
                    CallbackQueryHandler,inline_button_click_handler,ChatAction,handle_command_select_command,\
                    handle_info_command,handle_elite_command

from telegram.ext import CallbackContext
from saybot.file_upload import file_upload
import ssl

# Define an error handler function
def error_handler(update: Update, context: CallbackContext):
    # Log the exception details
    print(f"Exception occurred: {context.error}")

    # You can also send a message to the user or perform any other necessary actions

if __name__ == '__main__':
    try:

        # Code that interacts with SSL/TLS
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
         # my code
        application = Application.builder().token(token=os.getenv("API_BOT")).build()
        application.add_error_handler(error_handler)
        application.add_handler(CommandHandler('start',handle_start_command))
        application.add_handler(CommandHandler('info',handle_info_command))
        application.add_handler(CommandHandler('elite',handle_elite_command))

        application.add_handler(CommandHandler('chatgpt',handle_command_chatgpt)) # Model gpt-3.5-turbo used
        application.add_handler(CommandHandler('davincigpt',handle_command_davincigpt))
        application.add_handler(CommandHandler('image',handle_command_image_dalle2))
        application.add_handler(CommandHandler('uploadfile',handle_command_upload_file))
        application.add_handler(CommandHandler('askyourbook',handle_command_askyourbook))
        application.add_handler(CommandHandler('selectfile',handle_command_select_file))
        application.add_handler(CommandHandler('selectcommand',handle_command_select_command))

        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_message))
        # application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND,handle_message))
        application.add_handler(MessageHandler(filters.Document.MimeType("application/pdf"),file_upload))


        application.add_handler(CallbackQueryHandler(inline_button_click_handler))
        
        # Start the bot
        application.run_polling(1.0)
    except ssl.SSLWantReadError as e:
        # Handle SSL/TLS exception
        print("SSL/TLS exception occurred:", e)
    except ssl.SSLError as e:
        # Handle other SSL/TLS exceptions
        print("Other SSL/TLS exception occurred:", e)
    except Exception as e:
        # Handle other exceptions
        print("An error occurred:", e)
