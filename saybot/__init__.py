import openai

import logging
import os
import emoji
from typing import Any
from dotenv import load_dotenv
from pathlib import Path
from telegram import Bot,Update,InputMediaPhoto
from telegram.ext import Updater,CommandHandler,MessageHandler,filters,Application,ContextTypes,\
                  CallbackContext,CallbackQueryHandler
from datetime import datetime,timedelta
import sqlite3
import validators
import requests
import asyncio
from saybot.generate_response_textdavinchi003 import generate_response
from saybot.generate_response_gpt35turbo import generate_chat
from saybot.generate_image import generate_image

from saybot.store_user_data import store_user_data,store_prompt_quota,retrieve_index_dir,\
                      insert_file_data_database,retrieve_user_file_table,retrieve_chosen_file,retrieve_index_dir_from_fileid
from saybot.handler_prompt_quota import check_prompt_balance
# from generate_from_document import construct_index,generate_response_from_userdoc

from saybot.handle_prompt import handle_message
from saybot.handle_commands import handle_start_command,handle_command_gpt35turbo,handle_command_textdavinci003,\
                                    handle_command_image_dalle2,handle_command_upload_file,handle_command_askyourbook,\
                                    handle_command_select_file,inline_button_click_handler


# Set base directory and load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR,".env")
load_dotenv(dotenv_path)

# Configure logging
logging.basicConfig(level=logging.INFO)


__all__ = ['generate_response','handle_message','handle_start_command',\
           'generate_chat','generate_image','check_prompt_balance',\
            'handle_command_gpt35turbo','handle_command_textdavinci003',\
            'handle_command_image_dalle2','handle_command_upload_file','handle_command_askyourbook'
          ]