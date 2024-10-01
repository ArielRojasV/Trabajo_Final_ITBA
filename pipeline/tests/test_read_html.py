
import requests

def test_conexion():
   
    url = "https://iol.invertironline.com/Titulo/DatosHistoricos?simbolo=YPFD&mercado=BCBA" 

    req = requests.get(url)
 
    if req.status_code == 200:  # Validacion de estado de conexion
        print("URL Activa")


    
