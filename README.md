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
- Se generaron los métodos para extraer información de IOL a través del método read_html de pandas. Los datos consultados pertenecen a 5 empresas lideres, donde se obtiene los precios de acciones al inicio de la rueda, al final, el minimo, el máximo, los montos operados. El detalle pertence a los 2 ultimos años y se actualiza diariamente. Los datos no se pueden filtrar por fecha y se debe consultar cada cotización de forma independiente.


## Ejecución del proyecto
python extraccion.py
