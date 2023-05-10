
from saybot import Update, logging, datetime, sqlite3, os

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

    cursor.execute(  # DB for users file store
        '''CREATE TABLE IF NOT EXISTS user_file_table
            (
            id INTEGER ,
            date_of_upload DATE,
            file_name TEXT,
            file_id TEXT PRIMARY KEY,
            target_index_dir TEXT,
            file_title TEXT,
            file_summary TEXT
            )
            '''
    )


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
                cursor.execute("UPDATE usage_analysis SET last_accessed_time=:time,prompt_balance=:prompt_balance,prompt_quota=:prompt_quota WHERE id=:id",
                               prompt_data
                               )
                logging.info("User Prompt Data  updated in database")
            connection.commit()
        except Exception as e:
            logging.error(e)

        logging.info("DB connection is Closed:usage_analysis Table")


async def insert_file_data_database(update:Update,index_folder_path,**kwargs):

    logging.info("inside insert_file_data_databse")
    message = update.message
    file = update.message.document
    # logging.info("******data*******")
    # logging.info(kwargs.get("file_title"))
    # logging.info(kwargs.get("file_summary"))
    user_file_data = {
        "id":message.from_user.id,
        "date_of_upload":datetime.today() ,
        "file_name" :file.file_name,
        "file_id": file.file_id,
        "target_index_dir":index_folder_path ,
        "file_title": kwargs.get("file_title"),
        "file_summary":kwargs.get("file_summary")
    }

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT file_id FROM user_file_table WHERE file_id=?",(file.file_id,)
            )
            data = cursor.fetchone()
            if data is None: # no file data in table
                cursor.execute(
                    "INSERT INTO user_file_table (id,date_of_upload,file_name,file_id,target_index_dir,file_title,file_summary) VALUES (:id,:date_of_upload,:file_name,:file_id,:target_index_dir,:file_title,:file_summary)",
                    user_file_data
                )
                logging.info("New data added-user field table")
            else:
                cursor.execute("UPDATE user_file_table SET file_title=:file_title,file_summary=:file_summary WHERE file_id=:file_id",user_file_data)
                logging.info("data updated in user_file_table") #while update dont give prime key
            connection.commit()
        except Exception as e:
            logging.error(e)
    

def retrieve_index_dir(user_id):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT target_index_dir,file_name FROM user_file_table WHERE id=?",(user_id,)
            )
            data = cursor.fetchone()
            return data
        except Exception as e:
            logging.error(e)

def retrieve_index_dir_from_fileid(file_id):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT target_index_dir,file_name FROM user_file_table WHERE file_id=?",(file_id,)
            )
            data = cursor.fetchone()
            return data
        except Exception as e:
            logging.error(e)

def retrieve_user_file_table(userid):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT file_name,date_of_upload,file_title,file_summary,file_id FROM user_file_table WHERE id=?",(userid,)
            )
            data = cursor.fetchall()
            return data
        except Exception as e:
            logging.error(e)

def retrieve_chosen_file(file_id):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT file_name,date_of_upload,file_title,file_summary FROM user_file_table WHERE file_id=?",(file_id,)
            )
            data = cursor.fetchone()
            return data
        except Exception as e:
            logging.error(e)
