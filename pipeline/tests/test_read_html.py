
import requests
import config_extraccion as confext
from datetime import datetime

def test_conexion():
   
    url = "https://iol.invertironline.com/Titulo/DatosHistoricos?simbolo=YPFD&mercado=BCBA" 

    ##req = requests.get(url)
 
    ##assert req.status_code == 200  # Validacion de estado de conexion

    response = requests.get(url)
    if response.ok:   # alternatively you can use response.status_code == 200
        print("PaginaAccesible")
    else:
        print(f"Fallo, no se establecio conexion. Codigo : {response.status_code}")

       

def test_conexion_BCRA():

    response = requests.get(confext.obtener_datos_BCRA( confext.obtener_url_moneda_fechas("cotizaciones" , "USD" , datetime.today().strftime('%Y-%m-%d')  ,  datetime.today().strftime('%Y-%m-%d') ))) 

    if response.ok:   # alternatively you can use response.status_code == 200
        print("PaginaAccesible")
    else:
        print(f"Fallo, no se establecio conexion. Codigo : {response.status_code}")



