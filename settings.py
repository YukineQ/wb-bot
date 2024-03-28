import os
from dotenv import load_dotenv


BASEDIR = os.path.abspath(os.path.dirname(__file__))


dotenv_path = os.path.join(BASEDIR, '.env')
load_dotenv(dotenv_path)

EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
