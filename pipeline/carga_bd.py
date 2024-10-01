from sqlalchemy import create_engine
import pandas as pd

#################Variables de Conexion a Base de Datos##########################
redshift_user = "2024_ariel_rojas"
redshift_pass = "F9!L2^&6$xQ"
redshift_endpoint = "redshift-pda-cluster.cnuimntownzt.us-east-2.redshift.amazonaws.com"
port = 5439  
database = "pda"
#################Variables de Conexion a Base de Datos##########################
 

## defino datos de conexion
connection_string = f"postgresql://{redshift_user}:{redshift_pass}@{redshift_endpoint}:{port}/{database}"


def get_codigo_acciones(): 	

    engine = create_engine(connection_string)

    try:         
        connection = engine.raw_connection()   
        cursor = connection.cursor()

		#LLamo a tabla
        cursor.execute("""select desc_sigla from "2024_ariel_rojas_schema".lk_accion where id_flg_activo = 'S'""")   
        result = cursor.fetchall() 

        return [i[0].rstrip() for i in result] 

    finally: 
		
		#Cierro conexion 
        if connection: 
            cursor.close() 
            connection.close()   


## Carga datos a las tablas
def carga_dtf_to_bd(df, table): 
    
    engine = create_engine(connection_string)
    
    try:
        with engine.connect() as connection:
            print("Conexion Exitosa")            
            df.to_sql(name= table, con=engine, schema='2024_ariel_rojas_schema', if_exists='append', index=False)

    except Exception as e:
        print(f"Error conexion a Redshift: {e}")


def actualizar_ft_cotizaciones_bd():
    
    engine = create_engine(connection_string)
    connection = engine.raw_connection()   
    cursor = connection.cursor()
 
    with cursor:
        cursor.execute('CALL "2024_ariel_rojas_schema".sp_ft_cotizaciones_add()')
        connection.commit()
        cursor.close()  
        connection.close() 
     

def actualizar_stg_cotizaciones_monedas_bd():
    
    engine = create_engine(connection_string)
    connection = engine.raw_connection()   
    cursor = connection.cursor()
 
    with cursor:
        cursor.execute('CALL "2024_ariel_rojas_schema".sp_stg_cotizaciones_monedas_add()')
        connection.commit()
        cursor.close()  
        connection.close() 
    

def actualizar_stg_cotizaciones_acciones_bd():
    
    engine = create_engine(connection_string)
    connection = engine.raw_connection()   
    cursor = connection.cursor()
 
    with cursor:
        cursor.execute('CALL "2024_ariel_rojas_schema".sp_stg_cotizaciones_acciones_add()')
        connection.commit()
        cursor.close()  
        connection.close()  


def actualizar_lk_cotizacion_monedas_bd():
    
    engine = create_engine(connection_string)
    connection = engine.raw_connection()   
    cursor = connection.cursor()
 
    with cursor:
        cursor.execute('CALL "2024_ariel_rojas_schema".sp_lk_cotizacion_monedas_add()')
        connection.commit()
        cursor.close()  
        connection.close() 


