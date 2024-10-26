### Proyecto de Extracción y Carga de Datos Financieros

El objetivo de este proyecto es extraer información de las cotizaciones de una cartera de acciones en el mercado local, y también
se consultará información del BCRA relativa a ciertos indicadores financieros.

Los datos de las acciones corresponden a varias empresas que cotizan sus acciones en el mercado argentino. Los mismos se extraerán desde la página de InvertirOnline. Dicha extracción no se realizará a través de APIs.
Los datos del BCRA se consultarán a partir de las APIs públicas que posee la entidad (https://www.bcra.gob.ar/Catalogo/Content/files/pdf/estadisticascambiarias-v1.pdf).

## Esquema del Proyecto

![DiagramaExtraccion drawio (1)](https://github.com/user-attachments/assets/1c35481a-271d-4d80-a213-cfe6167ab9f5)


## Detalles del proyecto

- Se genero una instancia de Airflow en un contenedor de Docker, el cual orquestara las etapas de carga, transformación y procesamiento.
- Esta instancia de Airflow utiliza los DAG para definir la secuencialidad de las tareas.
- La primera tarea a realizar es la consulta a datos del BCRA (tipo de cambio), la cual se realiza por fecha, a partir de la ultima fecha cargada en la base de datos, se suma un dia y se consulta al endpoint de la entidad monetaria.
- La segunda tarea es leer los datos de las cotizaciones de acciones en el mercado argentino. El mismo se realiza haciendo Web Scrapping sobre la pagina de InvertirOnline. Desde aqui se leen datos de empresas lideres, donde se obtiene los precios de acciones al inicio de la rueda, al final, el minimo, el máximo, los montos operados. El detalle pertence a los 2 ultimos años y se actualiza diariamente. Los datos no se pueden filtrar por fecha y se debe consultar cada cotización de forma independiente. En este caso el filtrado de los datos se hace por código en Python, donde el método generado busca la ultima fecha cargada de cotizaciones cargadas en la base de datos. Esta fecha servirá para realizar el filtro en el dataframe obtenido desde la página de IOL para cargar solo los datos nuevos a la base de datos.
- A partir de estos datos se pretende armar una base de datos de cotización de acciones, con la cotización en moneda local y en dolares al tipo de cambio oficial del BCRA.

## Arquitectura de base de datos

Se simula contar con 3 instancias de bases de datos:

- Landing: en esta instancia se cargan los datos extraidos desde la API del BCRA y de la página de InvertirOnline, sin realizar modificaciones en la estructura.
- Staging: en esta instancia las entidades tienen definidos sus tipos de datos y se validan la unicidad de registros, la no existencia de valores nulos.
- Producción: la base que estará disponible para la consulta de los usuarios o el armado de reportes, cuenta con el siguiente modelo de datos:

    ![image](https://github.com/user-attachments/assets/e20f44ad-bf1a-47b9-81c6-868ae93edda9)

## Esquema de carpetas del proyecto

![image](https://github.com/user-attachments/assets/1f7a5aec-28f8-4887-a7c2-4575bd6512aa)


## Configuracion de la solución

1. Configurar el modelo en la base de datos.
   Para ello se debe ejecutar 3 scripts de bases de datos, en el orden que se menciona (carpeta scripts_bd):
   
   Script_Crear_Tablas.sql: genera el esquema de base de datos y las tablas a usar.

   Script_Generacion_Stores_Procedures.sql: agrega los Stores Procedures a utilizarse en la base de datos.

   Carga_Datos_lk_tcl_dia.sql: carga datos a la tabla lk_tcl_dia, pertenecientes a un calendario.

   Las credenciales de base de datos a utilizar, se envian las mismas en un archivo credenciales.txt:
   
    redshift_user = (redshift_user)
    redshift_pass = (redshift_pass) 
    redshift_endpoint = (redshift_endpoint)
    port = (port)
    database = (database)

2. Realizar el clonado de este repositorio:
   `https://github.com/ArielRojasV/Trabajo_Final_ITBA.git`

3. Dentro de la carpeta airflow/plugins crear un archivo .env con la informacion de las credenciales (copiar la informacion del archivo credenciales.txt). Ver esquema de la solución.

4. Ubicarse en la carpeta airflow y abrir una terminal.
   Ejecutar el comando:
   `docker compose build`

5. En Docker Desktop inicializar el contenedor
    ![image](https://github.com/user-attachments/assets/dadc6d43-082d-4be3-b52c-e651095938e6)

6. Abrir un navegador web y entrar a la siguiente URL:
  `http://localhost:8080/home`
   Credenciales:
   user: airflow
   password: airflow

7. Ejecutar el siguiente pipeline:
   `etl_pipeline`
