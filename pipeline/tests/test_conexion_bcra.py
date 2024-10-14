
import requests
from datetime import datetime


def test_conexion_BCRA():

    url = "https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones?fecha=" + datetime.today().strftime('%Y-%m-%d')

    response = requests.get(url)

    if response.ok:   
        print("Pagina Accesible")
    else:
        print(f"Fallo, no se establecio conexion. Codigo : {response.status_code}")
