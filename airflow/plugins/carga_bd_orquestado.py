from sqlalchemy import create_engine
import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("redshift_user")
pasw = os.getenv("redshift_pass")
endp = os.getenv("redshift_endpoint")
port = os.getenv("port")
dbase = os.getenv("database")   

REDSHIFT_SCHEMA = '"2024_ariel_rojas_schema"'

## Defino datos de conexion
connection_string = f"postgresql://{user}:{pasw}@{endp}:{port}/{dbase}"
engine = create_engine(connection_string)


## Carga datos a las tablas
def carga_dtf_to_bd(df, table): 
    
    try:
        with engine.connect() as connection:
            #print("Conexion Exitosa")            
            df.to_sql(name= table, con=engine, schema='2024_ariel_rojas_schema', if_exists='append', index=False)

    except Exception as e:
        print(f"Error conexion a Redshift: {e}")



def get_fechaultima_cotizacion_accion(): 	   

    try:         
        connection = engine.raw_connection()   
        cursor = connection.cursor() 
       
		#LLamo a tabla
        cursor.execute(f"""select max(dia.desc_tcl_dia) from {REDSHIFT_SCHEMA}.ft_cotizaciones ftc
                            inner join {REDSHIFT_SCHEMA}.lk_tcl_dia dia
                            on ftc.id_tcl_dia = dia.id_tcl_dia""") 
        result = cursor.fetchall() 

        return [i[0] for i in result] 

    finally: 
		
		#Cierro conexion 
        if connection: 
            cursor.close() 
            connection.close() 



def get_fechaultima_cotizacion_moneda(): 	

    try:         
        connection = engine.raw_connection()   
        cursor = connection.cursor()

		#LLamo a tabla de base de datos
        cursor.execute(f"""select max(dia.desc_tcl_dia) from {REDSHIFT_SCHEMA}.lk_cotizacion_monedas lcm 
                            inner join {REDSHIFT_SCHEMA}.lk_tcl_dia dia
                            on lcm.id_tcl_dia = dia.id_tcl_dia""")   
        result = cursor.fetchall() 

        return [i[0] for i in result] 

    finally: 
		
		#Cierro conexion 
        if connection: 
            cursor.close() 
            connection.close() 
 


def get_codigo_acciones(): 	

    try:         
        connection = engine.raw_connection()   
        cursor = connection.cursor()

		#LLamo a tabla
        cursor.execute(f"select desc_sigla from {REDSHIFT_SCHEMA}.lk_accion where id_flg_activo = 'S'")   
        result = cursor.fetchall() 

        return [i[0].rstrip() for i in result] 

    finally: 
		
		#Cierro conexion 
        if connection: 
            cursor.close() 
            connection.close()   



def actualizar_ft_cotizaciones_bd():

    try:
        connection = engine.raw_connection()   
        cursor = connection.cursor()
 
        with cursor:
            cursor.execute(f'CALL {REDSHIFT_SCHEMA}.sp_ft_cotizaciones_add()')
            connection.commit()

    finally: 
		
		#Cierro conexion 
        if connection: 
            cursor.close() 
            connection.close()   
     


def actualizar_stg_cotizaciones_monedas_bd():

    try:    
        connection = engine.raw_connection()   
        cursor = connection.cursor()
 
        with cursor:
            cursor.execute(f'CALL {REDSHIFT_SCHEMA}.sp_stg_cotizaciones_monedas_add()')            
            connection.commit()
    
    finally: 
		
		#Cierro conexion 
        if connection: 
            cursor.close() 
            connection.close()
    


def actualizar_stg_cotizaciones_acciones_bd():

    try:
        connection = engine.raw_connection()   
        cursor = connection.cursor()
 
        with cursor:
            cursor.execute(f'CALL {REDSHIFT_SCHEMA}.sp_stg_cotizaciones_acciones_add()')
            connection.commit()

    finally: 
		
		#Cierro conexion 
        if connection: 
            cursor.close() 
            connection.close()
 


def actualizar_lk_cotizacion_monedas_bd():
    
    try:
        connection = engine.raw_connection()   
        cursor = connection.cursor()
 
        with cursor:
            cursor.execute(f'CALL {REDSHIFT_SCHEMA}.sp_lk_cotizacion_monedas_add()')
            connection.commit()

    finally: 
		
		#Cierro conexion 
        if connection: 
            cursor.close() 
            connection.close()


