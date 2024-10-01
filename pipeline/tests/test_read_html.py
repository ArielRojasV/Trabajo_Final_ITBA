
import requests

def test_conexion():
   
    url = "https://iol.invertironline.com/Titulo/DatosHistoricos?simbolo=YPFD&mercado=BCBA" 

    req = requests.get(url)
 
    assert req.status_code == 200  # Validacion de estado de conexion
       

    
