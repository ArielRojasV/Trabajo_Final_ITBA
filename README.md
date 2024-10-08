### Proyecto de Extracción y Carga de Datos Financieros

El objetivo de este proyecto es extraera info de las cotizaciones de una cartera de acciones tanto locales como del exterior, y también
se consultará información del BCRA relativa a ciertos indicadores financieros.

Los datos de las acciones corresponden a 5 empresas y se extraerán desde la página de InvertirOnline. Dicha extracción no se realizará a través de APIs.
Los datos del BCRA se consultarán a partir de las APIs públicas que posee la entidad (https://www.bcra.gob.ar/Catalogo/Content/files/pdf/estadisticascambiarias-v1.pdf).

## Esquema del Proyecto

![DiagramaExtraccion drawio (1)](https://github.com/user-attachments/assets/1c35481a-271d-4d80-a213-cfe6167ab9f5)


## Detalles del proyecto
- Se genero una instancia de Airflow en un contenedor de Docker, el cual orquestara las etapas de carga, transformación y procesamiento.
- Esta instancia de Airflow utiliza los DAG para definir la secuencialidad de las tareas.
- La primera tarea a realizar es la consulta a datos del BCRA (tipo de cambio), la cual se realiza por fecha, a partir de la ultima fecha cargada en la base de datos, se suma un dia y se consulta al endpoint de la entidad monetaria. Los datos extraidos se cargan a una base de datos de "Landing".
- La segunda tarea es leer los datos de las cotizaciones de acciones en el mercado argentino. El mismo se realiza haciendo Web Scrapping sobre la pagina de InvertirOnline. Desde aqui se leen datos de empresas lideres, donde se obtiene los precios de acciones al inicio de la rueda, al final, el minimo, el máximo, los montos operados. El detalle pertence a los 2 ultimos años y se actualiza diariamente. Los datos no se pueden filtrar por fecha y se debe consultar cada cotización de forma independiente. En este caso el filtrado de los datos se hace en el código, dado que el método generado en Python busca la ultima fecha con cotizaciones cargadas en la base de datos y filtra los resultados obtenidos para cargar solo los datos nuevos.


## Ejecución del proyecto
python extraccion.py
