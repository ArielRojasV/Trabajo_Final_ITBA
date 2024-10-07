 
from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator 

from extraccion_orquestado import extraer_datos_BCRA, extraer_datos_IOL, carga_staging, carga_produccion
 
with DAG(
    'etl_pipeline' ,
    default_args={
        'depends_on_past' :  False,
        'email_on_failure' : False,
        'email_on_retry': False,
        'retries': 1,
    },
    description = 'ETL',
    schedule_interval='@daily',
    start_date=datetime(2024,10,4),
    catchup = False

) as dag:
    

    extraccion_BCRA = PythonOperator(
        task_id='Extraccion_BCRA',
        python_callable = extraer_datos_BCRA
    )   


    extraccion_IOL = PythonOperator(
        task_id='Extraccion_IOL',
        python_callable = extraer_datos_IOL
        )


    carga_en_staging_bd = PythonOperator(
        task_id='Carga_Staging',
        python_callable = carga_staging
    )


    carga_en_produccion_bd = PythonOperator(
        task_id='Carga_Produccion',
        python_callable = carga_produccion
    )


##Orden de los tasks
extraccion_BCRA >> extraccion_IOL >> carga_en_staging_bd >> carga_en_produccion_bd
