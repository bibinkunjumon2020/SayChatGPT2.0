from saybot import Update,ContextTypes,logging,datetime,os,asyncio,insert_file_data_database,ChatAction
from saybot.config import ConfigClass
from saybot.generate_from_document import construct_index,generate_response_from_userdoc

from saybot.select_file_config import SelectFileClass

async def create_folder_for_file(file_id,file_name):
    source_file_dir = "source_dir"  # source of all files
    if not os.path.exists(source_file_dir):
        os.makedirs(source_file_dir)
    source_file_path = os.path.join(source_file_dir,file_name)

    target_file_dir = "target_dir"
    if not os.path.exists(target_file_dir):
        os.makedirs(target_file_dir)

    target_dir_index_folder = f"index_{file_id}"
    index_folder_path = os.path.join(target_file_dir, target_dir_index_folder)
    os.makedirs(index_folder_path)

    return index_folder_path,source_file_path

# Checkinf the pdf upload is with in the limit
async def file_upload_size_check(update, context):
    document = update.message.document
    file_size_limit = 10 * 1024 * 1024  # 10 MB FIle size allowed

    if document.mime_type == 'application/pdf' and document.file_size > file_size_limit:
        # Handle the case when the file size exceeds the limit
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, the uploaded PDF document exceeds the file size limit.")
        logging.info("The uploaded PDF document exceeds the file size limit")
        return False

    return True

# upload file from user,index creation method call,delete uploaded file,store file details in db
async def file_upload(update: Update, context: ContextTypes.DEFAULT_TYPE): #its a command handler
    await context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.UPLOAD_DOCUMENT)
    logging.info("**** Inside File Upload ****")
    model_selection_command = ConfigClass.get_model_selection_command()
    print("------------", model_selection_command)
    try:
        if model_selection_command == "uploadfile":  # /uploadfile command must be run before the file upload
            user_uploaded_file = update.message.document
            if user_uploaded_file.mime_type == "application/pdf":
                upload_date = datetime.today()
                file_size_limit = await file_upload_size_check(update=update,context=context)
                if file_size_limit is False:
                    return
                # this unique id can be used for reuse of file
                file_id = user_uploaded_file.file_id
                file_name = user_uploaded_file.file_name
                # it returns file
                new_file = await context.bot.get_file(file_id=file_id)

                print(
                    f"file-name:{file_name} & file-id:{file_id} & file-size: {new_file.file_size}& Upload-date:{upload_date}")

                index_folder_path,source_file_path = await create_folder_for_file(file_id=file_id,file_name=file_name)
                
                download_task = asyncio.ensure_future(new_file.download_to_drive(source_file_path))  # start coroutine background
                logging.info('PDF file saved successfully!')
                await update.message.reply_text(reply_to_message_id=update.message.id,text="PDF file saved successfully!")
                # context.job_queue.run_once(construct_index)
                await download_task # wait for coroutine to complete
                index_task = asyncio.create_task(construct_index(source_dir= "source_dir",index_folder_path = index_folder_path))    # start coroutine background
                await index_task  # wait for coroutine to complete
                insert_db = asyncio.create_task(insert_file_data_database(update=update,index_folder_path=index_folder_path))
                
                file_id_selected = SelectFileClass.get_select_file_id()#storing currently using file_id
                SelectFileClass.set_select_file_id(file_id) # id is set for running following prompts

                await insert_db # wait for coroutine to complete
                file_title = generate_response_from_userdoc(prompt="generate very short title",update=update)
                file_summary =generate_response_from_userdoc(prompt="generate very short summary",update=update)
                asyncio.create_task(insert_file_data_database(update=update,index_folder_path=index_folder_path,file_title=file_title,file_summary=file_summary))
                os.remove(source_file_path) # Removed the uploaded file after usage
                SelectFileClass.set_select_file_id(file_id_selected)#setting back currently using file_id
                #disabling the file upload after One file.User cannt upload now.
                ConfigClass.set_model_selection_command("selectcommand") 
            else:
                await update.message.reply_text(reply_to_message_id=update.message.id, text="'Please upload a PDF format file.'")

        else:
            await update.message.reply_text(reply_to_message_id=update.message.id, text="Only Text Input is allowed under this Command")

    except Exception as e:
        print(e)