import sqlite3
from saybot import Update, logging

# create table if not exists
with sqlite3.connect('user_data.db') as connection:
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             chat_id INTEGER,username TEXT, 
             first_name TEXT, last_name TEXT,location TEXT)''')

async def store_user_data(update: Update):
    user_data = {
        "id": update.message.from_user.id,
        "chat_id": update.message.chat_id,
        "username": update.message.from_user.username,
        "first_name": update.message.from_user.first_name,
        "last_name": update.message.from_user.last_name,
        "location": update.message.chat.location,
    }

    with sqlite3.connect('user_data.db') as connection:
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

        logging.info("DB connection is Closed")
