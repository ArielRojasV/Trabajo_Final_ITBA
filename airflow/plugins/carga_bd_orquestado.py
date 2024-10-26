from sqlalchemy import create_engine
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

##Variable esquema de base de datos
REDSHIFT_SCHEMA = '"2024_ariel_rojas_schema"'

## Defino datos de conexion
def conexion_to_bd():
    user = os.getenv("redshift_user")
    pasw = os.getenv("redshift_pass")
    endp = os.getenv("redshift_endpoint")
    port = os.getenv("port")
    dbase = os.getenv("database") 

    connection_string = f"postgresql://{user}:{pasw}@{endp}:{port}/{dbase}"
    engine = create_engine(connection_string)
    return engine


##Cierro sesion
def cierroconexion_to_bd(cursor, connection):
    cursor.close() 
    connection.close() 


##Queries a ejecutar en base de datos obteniendo fechas
def query_ult_fecha_entidad(tabla)
    match tabla:
        case "accion": 
            return (f"""select max(dia.desc_tcl_dia) from {REDSHIFT_SCHEMA}.ft_cotizaciones ftc
                            inner join {REDSHIFT_SCHEMA}.lk_tcl_dia dia
                            on ftc.id_tcl_dia = dia.id_tcl_dia""")
        case "moneda":
            return (f"""select max(dia.desc_tcl_dia) from {REDSHIFT_SCHEMA}.lk_cotizacion_monedas lcm 
                            inner join {REDSHIFT_SCHEMA}.lk_tcl_dia dia
                            on lcm.id_tcl_dia = dia.id_tcl_dia""")   


## Carga datos a las tablas
def carga_dtf_to_bd(df, table): 
    connection = conexion_to_bd().connect()  

    try:
        with connection:          
            df.to_sql(name= table, con=conexion_to_bd(), schema='2024_ariel_rojas_schema', if_exists='append', index=False)

    except Exception as e:
        print(f"Error conexion a Redshift: {e}")
        raise


##Codigo que identifica cada accion en IOL
def get_codigo_acciones(): 	
    try:         
        connection = conexion_to_bd().raw_connection()  
        cursor = connection.cursor()
        
        cursor.execute(f"select desc_sigla from {REDSHIFT_SCHEMA}.lk_accion where id_flg_activo = 'S'")   
        result = cursor.fetchall() 
        return [i[0].rstrip() for i in result] 

    finally: 
        if connection: 
            cierroconexion_to_bd(cursor, connection)


##Ultima fecha de dato cargado en la base de datos segun entidad
def get_fechaultima_entidad_bd(entidad):  
    try:         
        connection = conexion_to_bd().raw_connection()   
        cursor = connection.cursor() 
    
        query = query_ult_fecha_entidad(entidad)

        cursor.execute(query) 
        result = cursor.fetchall() 
        return [i[0] for i in result] 

    finally: 		 
        if connection: 
            cierroconexion_to_bd(cursor, connection)


##Ejecutar Store Procedure de ambiente Staging
def ejecutar_sp_staging_bd(store_proc):    
    try:
        connection = conexion_to_bd().raw_connection() 
        cursor = connection.cursor()
 
        with cursor:
            cursor.execute(f'CALL {REDSHIFT_SCHEMA}.{store_proc}')
            connection.commit()

    finally: 		
        if connection: 
            cierroconexion_to_bd(cursor, connection) 


##Ejecutar Store Procedure de ambiente produccion
def ejecutar_sp_produccion_bd(store_proc):    
    try:
        connection = conexion_to_bd().raw_connection() 
        cursor = connection.cursor()
 
        with cursor:
            cursor.execute(f'CALL {REDSHIFT_SCHEMA}.{store_proc}')
            connection.commit()

    finally: 		
        if connection: 
            cierroconexion_to_bd(cursor, connection) 



