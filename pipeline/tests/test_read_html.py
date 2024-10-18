import unittest
from unittest.mock import patch 
from typing import Dict
import requests


def get_data_Json(url: str) -> Dict[str, str]:
    response = requests.get(url)
    return response.json()


class Test_Get_Data_Json(unittest.TestCase):
    @patch('requests.get')
    def test_get_data(self, mock_get):
        mock_response = mock_get.return_value  
        mock_response.json.return_value = {'fechacotizacion': '01/01/2020',
                                            'cierre' : '1000'}  
        
        url = "https://iol.invertironline.com/Titulo/DatosHistoricos?simbolo=YPFD&mercado=BCBA" 
        result =  get_data_Json(url)  
        
        self.assertEqual(result, {'fechacotizacion': '01/01/2020',
                                            'cierre' : '1000'})  
        mock_get.assert_called_once_with(url)  


"""
apertura
máximo
mínimo
cierre
cierreajustado
volumenmonto
volumennominal
"""