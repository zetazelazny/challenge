import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from datetime import date
from decouple import config
from constants import LOG_FILE
import logging

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode="w", 
                    format="%(asctime)s - %(levelname)s - %(message)s")


def download_file(file_url, file_path):
    logging.info(f"Descargando archivo {file_path}")
    logging.info(f"Ruta de origen: {file_url}")
    
    file_exists = os.path.exists(file_path)
    if file_exists:
        os.remove(file_path)
    with requests.get(file_url) as req:
        with open(file_path, 'wb') as file:
            file.write(req.content)

def create_path(path_name):
    path_exists = os.path.exists(path_name)
    if not path_exists:
        try:
            os.makedirs(path_name)
            logging.info(f"Directorio {path_name} creado")
        except:
            logging.error(f"Error al intentar crear el directorio {path_name}")
    else:
        logging.info(f"Ya existe el directorio {path_name}")

def get_data_frame(path, file_name):
    file_data = pd.read_csv (path + "\\" + file_name)
    dataframe = pd.DataFrame(file_data)
    logging.info(f"Creando DataFrame desde archivo {file_name}")
    return dataframe

def get_engine(user, pwd, host, port, db):
    url = f"postgresql://{user}:{pwd}@{host}:{port}/{db}"
    logging.info(f"Creando engine para conexion a postgres")
    logging.info(f"URL: {url}")
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine

def get_engine_from_settings():   
    return get_engine(config('PGUSER'), config('PGPWD'), config('PGHOST'), config('PGPORT'), config('PGDB'))

def get_session():
    engine = get_engine_from_settings()
    session = sessionmaker(bind=engine) ()
    return session

def insert_dataframe_to_db(dataframe, table_name, engine, condition):
    logging.info(f"Insertando DataFrame en la tabla {table_name}")
    try:
        dataframe.to_sql(table_name, con = engine, if_exists=condition)
        logging.info(f"DataFrame insertado con exito en la tabla {table_name}")
    except:
        logging.error(f"Se produjo un error al insertar el DataFrame")

def add_load_date(dataframe):
    dataframe['FECHA_CARGA'] = date.today().strftime("%d-%m-%Y")
    return dataframe