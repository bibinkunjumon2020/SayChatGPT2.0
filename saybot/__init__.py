import openai

import logging
import os
import emoji
from typing import Any
from dotenv import load_dotenv
from pathlib import Path
from telegram import Bot,Update,InputMediaPhoto
from telegram.ext import Updater,CommandHandler,MessageHandler,filters,Application,ContextTypes
from datetime import datetime,timedelta
import sqlite3

from saybot.generate_response_textdavinchi003 import generate_response
from saybot.generate_response_gpt35turbo import generate_chat
from saybot.generate_image import generate_image

from saybot.store_user_data import store_user_data,store_prompt_quota
from saybot.handler_prompt_quota import check_prompt_balance

from saybot.handle_prompt import handle_message
from saybot.handle_commands import handle_start_command,handle_command_gpt35turbo,handle_command_textdavinci003


# Set base directory and load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR,".env")
load_dotenv(dotenv_path)

# Configure logging
logging.basicConfig(level=logging.INFO)


__all__ = ['generate_response','handle_message','handle_start_command',\
           'generate_chat','generate_image','check_prompt_balance',\
            'handle_command_gpt35turbo','handle_command_textdavinci003',
          ]