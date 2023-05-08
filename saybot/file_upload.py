from saybot import Update,ContextTypes,logging,datetime,os,asyncio,insert_file_data_database
from saybot.config import ConfigClass
from saybot.generate_from_document import construct_index,generate_response_from_userdoc

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


# upload file from user,index creation method call,delete uploaded file,store file details in db
async def file_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("**** Inside File Upload ****")
    model_selection_command = ConfigClass.get_model_selection_command()
    print("------------", model_selection_command)
    try:
        if model_selection_command == "uploadfile":  # /uploadfile command must be run before the file upload
            user_uploaded_file = update.message.document
            upload_date = datetime.today()
            if user_uploaded_file.mime_type == "application/pdf":
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
                await insert_db # wait for coroutine to complete
                file_title = generate_response_from_userdoc(prompt="generate one line title",update=update)
                file_summary =generate_response_from_userdoc(prompt="generate short summary",update=update)
                asyncio.create_task(insert_file_data_database(update=update,index_folder_path=index_folder_path,file_title=file_title,file_summary=file_summary))
                os.remove(source_file_path) # Removed the uploaded file after usage
            else:
                await update.message.reply_text(reply_to_message_id=update.message.id, text="'Please send a PDF file.'")

        else:
            await update.message.reply_text(reply_to_message_id=update.message.id, text="Only Text Input is allowed under this Command")

    except Exception as e:
        print(e)