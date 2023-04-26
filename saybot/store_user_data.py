
from saybot import Update, logging,datetime,sqlite3,os

# create table if not exists
db_path = os.path.join(os.getcwd(),"database","user_data.db")

with sqlite3.connect(db_path) as connection:
    cursor = connection.cursor()                # This Store User Information
    cursor.execute('''CREATE TABLE IF NOT EXISTS users     
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             chat_id INTEGER,username TEXT, 
             first_name TEXT, last_name TEXT,location TEXT)'''
    )

    cursor.execute(   # This Store User Quota,Balance,Last access time Information
        '''CREATE TABLE IF NOT EXISTS usage_analysis 
        (id INTEGER PRIMARY KEY,last_accessed_time DATETIME,prompt_balance INTEGER,prompt_quota INTEGER)
        '''
    )

async def store_user_data(update: Update):
    user_data = {               #Dictionary for pushing into users table user_dataDB
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
            cursor.execute("SELECT id FROM users WHERE id=?", (user_data['id'],))
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
async def store_prompt_quota(update:Update,**args):

    logging.info("inside store_prompt_quota")
    
    prompt_data={                             #Dictionary for pushing into User_analysis table user_dataDB
        "id":update.message.from_user.id,
        "time":datetime.now(),
        'prompt_balance':args.get('prompt_balance'),
        "prompt_quota":args.get('prompt_quota')
    }
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT id FROM usage_analysis WHERE id=?",(prompt_data.get("id"),))
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