from saybot import Update,timedelta,datetime,sqlite3,logging,store_prompt_quota


async def check_prompt_balance(update:Update): # daily prompt limit is defined and managed
    user_id = update.message.from_user.id # individual user IDs
    prompt_quota=10 # manually fixing it
    
    with sqlite3.connect('user_data.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM usage_analysis WHERE id=?",(user_id,))  #accessing this users entry
        data = cursor.fetchone()
      
        try:
            if data is not None :
                prompt_balance = data[2]  
                prompt_quota = data[3]
                #time data need to convert from string in DB to datetime format.
                last_accessed_time = datetime.strptime(data[1],'%Y-%m-%d %H:%M:%S.%f')
                now = datetime.now() 
                if(now - last_accessed_time) < timedelta(hours=24) and prompt_balance <= 0 :# checking 24 hr and prompt balance
                    logging.info("Prompt Quota Finished Promt Balance = "+str(prompt_balance))
                    return False
                elif(now-last_accessed_time) >= timedelta(hours=24):      # If 24 hr crossed from last usage:Recharge Balance
                    prompt_balance=prompt_quota  # recharged the prompt balance
                    await store_prompt_quota(update=update,prompt_balance = prompt_balance,prompt_quota=prompt_quota)
                    logging.info(" Recharged Prompt Balance = "+str(prompt_balance))
                    return True
                else:
                    prompt_balance -= 1 # reducing the prompt balance by '1'
                    await store_prompt_quota(update=update,prompt_balance = prompt_balance,prompt_quota=prompt_quota)
                    return True

            else:#data is none - User is for the first time
                prompt_balance = prompt_quota - 1 # reducing the prompt balance by '1'
                await store_prompt_quota(update=update,prompt_balance = prompt_balance,prompt_quota=prompt_quota)
                return True
        except Exception as e:
            logging.error(e)
