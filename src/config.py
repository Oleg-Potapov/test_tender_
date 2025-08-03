from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


BASE_URL = os.environ.get('BASE_URL')
DB_PATH = os.environ.get('DB_PATH')
URL = os.environ.get('URL')
