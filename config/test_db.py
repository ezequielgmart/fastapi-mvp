import os
from pygem.main import create_db_pool
from dotenv import load_dotenv

# load the env variables from the  .env file
load_dotenv()



# Configuración de la base de datos
CONFIG = {
    'user': os.getenv('TEST_DB_USER'),
    'password': os.getenv('TEST_DB_PASSWORD'),
    'database': os.getenv('TEST_DB_NAME'),
    'host': os.getenv('TEST_DB_HOST'),
    'port': int(os.getenv('TEST_DB_PORT'))
}
