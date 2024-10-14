 
import requests
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('redshift_user')
pasw = os.getenv('redshift_pass')
endp = os.getenv('redshift_endpoint')
port = os.getenv('port')
dbase = os.getenv('database')
   
## defino datos de conexion
connection_string = f"postgresql://{user}:{pasw}@{endp}:{port}/{dbase}" 
 
engine = create_engine(connection_string)

try:         
    connection = engine.raw_connection()   
    cursor = connection.cursor()

    cursor.execute("SELECT VERSION()")
    resultado = cursor.fetchone()
    version = resultado[0]

    if(version is not None):
        print("Base de datos Accesible")
    else:
        print("Base de datos No Accesible")
         
except:
    print(f"Fallo, no se establecio conexion")
