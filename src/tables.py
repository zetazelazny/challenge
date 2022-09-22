import psycopg2
from constants import SQL_FILE
from decouple import config

def create_tables():
    conn = psycopg2.connect(user=config('PGUSER'), 
                            password=config('PGPWD'), 
                            host=config('PGHOST'), 
                            port=config('PGPORT'), 
                            database=config('PGDB'))
    cursor = conn.cursor()
    sqlfile = open(SQL_FILE, 'r')
    cursor.execute(sqlfile.read())
    conn.commit()
    conn.close()