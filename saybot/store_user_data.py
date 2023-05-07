
from saybot import Update, logging, datetime, sqlite3, os, ContextTypes
from saybot.config import ConfigClass
from saybot.generate_from_document import construct_index
import asyncio

# create table if not exists
db_directory = os.path.join(os.getcwd(), "database")
os.makedirs(db_directory, exist_ok=True)
db_path = os.path.join(os.getcwd(), "database", "user_data.db")


with sqlite3.connect(db_path) as connection:
    cursor = connection.cursor()                # This Store User Information
    cursor.execute('''CREATE TABLE IF NOT EXISTS users     
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             chat_id INTEGER,
             username TEXT, 
             first_name TEXT, 
             last_name TEXT,
             location TEXT)'''
    )

    cursor.execute(   # This Store User Quota,Balance,Last access time Information
        '''CREATE TABLE IF NOT EXISTS usage_analysis 
        (id INTEGER PRIMARY KEY,
        last_accessed_time DATETIME,
        prompt_balance INTEGER,
        prompt_quota INTEGER)
        '''
    )

    # cursor.execute(  # DB for user individual book store
    #     '''CREATE TABLE IF NOT EXISTS user_book_table
    #         (id INTEGER PRIMARY KEY,
    #         date_of_upload DATE,
    #         book_name TEXT,
    #         book_file BINARY
    #         )
    #         '''
    # )


async def store_user_data(update: Update):
    user_data = {  # Dictionary for pushing into users table user_dataDB
        "id": update.message.from_user.id,
        "chat_id": update.message.chat_id,
        "username": update.message.from_user.username,
        "first_name": update.message.from_user.first_name,
        "last_name": update.message.from_user.last_name,
        "location": update.message.chat.location,
    }

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT id FROM users WHERE id=?",
                           (user_data['id'],))
            data = cursor.fetchone()

            if data is None:
                # user is not in database,insert user into db
                cursor.execute("INSERT INTO users (id,chat_id,username,first_name,last_name,location) VALUES (:id,:chat_id,:username,:first_name,:last_name,:location)",
                               user_data)
                logging.info("User data inserted into database")
            else:
                cursor.execute("UPDATE users SET chat_id=:chat_id,username=:username,first_name=:first_name,last_name=:last_name,location=:location WHERE id=:id",
                               user_data)
                logging.info("User data updated in database")

            connection.commit()
        except Exception as e:
            logging.error(e)

        logging.info("DB connection is Closed :users Table")

# Table For handling the Usage analytics data


async def store_prompt_quota(update: Update, **args):

    logging.info("inside store_prompt_quota")

    prompt_data = {  # Dictionary for pushing into User_analysis table user_dataDB
        "id": update.message.from_user.id,
        "time": datetime.now(),
        'prompt_balance': args.get('prompt_balance'),
        "prompt_quota": args.get('prompt_quota')
    }
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT id FROM usage_analysis WHERE id=?", (prompt_data.get("id"),))
            data = cursor.fetchone()
            if data is None:
                # user is not in database,insert user into db
                cursor.execute("INSERT INTO usage_analysis (id,last_accessed_time,prompt_balance,prompt_quota) VALUES  (:id,:time,:prompt_balance,:prompt_quota)",
                               prompt_data)
                logging.info("User Prompt Data inserted into database")
            else:
                cursor.execute("UPDATE usage_analysis SET id=:id,last_accessed_time=:time,prompt_balance=:prompt_balance,prompt_quota=:prompt_quota WHERE id=:id",
                               prompt_data
                               )
                logging.info("User Prompt Data  updated in database")
            connection.commit()
        except Exception as e:
            logging.error(e)

        logging.info("DB connection is Closed:usage_analysis Table")


async def file_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("**** Inside File Upload ****")
    model_selection_command = ConfigClass.get_model_selection_command() 
    print("------------",model_selection_command) 
    try:
        if model_selection_command == "uploadfile": #/uploadfile command must be run before the file upload
            user_uploaded_file = update.message.document
            if user_uploaded_file.mime_type == "application/pdf":
                file_id = user_uploaded_file.file_id  # this unique id can be used for reuse of file
                file_name = user_uploaded_file.file_name
                new_file = await context.bot.get_file(file_id=file_id) # it returns file

                source_dir = "source_dir"  # source of all files
                if not os.path.exists(source_dir):
                    os.makedirs(source_dir)
                    
                save_path = os.path.join(source_dir,file_name)
                asyncio.ensure_future(new_file.download_to_drive(save_path))  # start coroutine background 
                logging.info('PDF file saved successfully!')
                await update.message.reply_text(reply_to_message_id=update.message.id,text="PDF file saved successfully!")
                # context.job_queue.run_once(construct_index)
                asyncio.create_task(construct_index())    # start coroutine background 
            else:
                await update.message.reply_text(reply_to_message_id=update.message.id,text="'Please send a PDF file.'")

        else:
            await update.message.reply_text(reply_to_message_id=update.message.id,text="Only Text Input is allowed under this Command")

    except Exception as e:
        print(e)



    # try:
    
    #     book_name= update.message.document.file_name
        
    #     with open(book_name, "rb") as f:
    #         while True:
    #             chunk = f.read(1024)
    #             if not chunk:
    #                 break
    #             # Do something with the chunk


    # except Exception as e:
    #     logging.error(e)



    # book_field = {
    #     "id": update.message.from_user.id,
    #     "date_of_upload": datetime.today(),
    #     "book_name": book_name,
    #     "book_file" : update.message.document.file_contents,
    # }

    # with sqlite3.connect(db_path) as connection:
    #     cursor = connection.cursor()
    #     try:

    #         cursor.execute(
    #             "INSERT INTO user_book_table (id,date_of_upload,book_name,book_file) VALUES (:id,:date_of_upload,:book_name,:book_file)",
    #             book_field
    #         )
    #     except Exception as e:
    #         logging.error(e)
