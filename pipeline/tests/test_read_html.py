import unittest
from unittest.mock import patch , MagicMock
from typing import Dict
import requests
import pandas as pd


def get_data_Json(url: str):
    response = requests.get(url)
    return response.json()


class Test_Get_Data_Json(unittest.TestCase):
    @patch('requests.get')
    def test_get_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200       
        mock_response = mock_get.return_value  

        mock_response.json.return_value = {"fechacotizacion": "2024-01-01",
                                           "apertura": "975.00",
                                           "maximo" : "1050.00",
                                           "minimo" : "950.00",
                                           "cierre" : "1000.00",
                                           "cierreajustado" : "1010.00"                                           
                                            }  
       
       # Simulo URL                            
        url = 'http://IOL.com/'

        # Simulo Llamada API 
        resultado = get_data_Json(url)
        resultado = pd.json_normalize( resultado )

        # Resultado Esperado
        resultado_esperado = pd.DataFrame([{'fechacotizacion': '2024-01-01',
                                           'apertura': '975.00',
                                           'maximo' : '1050.00',
                                           'minimo' : '950.00',
                                           'cierre' : '1000.00',
                                           'cierreajustado' : '1010.00'                                           
                                            }])
        
        # Testeo si son iguales
        pd.testing.assert_frame_equal(resultado, resultado_esperado )
         
  