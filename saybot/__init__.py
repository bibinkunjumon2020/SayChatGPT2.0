import openai

import logging
import os
import emoji
from dotenv import load_dotenv
from pathlib import Path
from telegram import Bot,Update,InputMediaPhoto
from telegram.ext import Updater,CommandHandler,MessageHandler,filters,Application,ContextTypes
from datetime import datetime,timedelta

from saybot.generate_response import generate_response
from saybot.handle_prompt import handle_message
from saybot.handle_start import handle_start_command

# Set base directory and load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(BASE_DIR,".env")
load_dotenv(dotenv_path)

# Configure logging
logging.basicConfig(level=logging.INFO)



__all__ = ['generate_response','handle_message','handle_start_command']