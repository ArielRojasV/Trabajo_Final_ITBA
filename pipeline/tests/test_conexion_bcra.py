import requests
import unittest
import json
from unittest.mock import patch, Mock, MagicMock


def get_data_bcra():
    response = requests.get("https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones?" )    
    data = json.loads(response.text)
    return data

class Test_Get_Data(unittest.TestCase):
    @patch('main.get_data_bcra')
    def test_get_data_bcra(self, mock_get_data):
        mock_data = {"codigoMoneda":"USD",
                    "descripcion":"DOLAR E.E.U.U.",
                    "tipoPase":0.00000000,
                    "tipoCotizacion":1000}
        
        mock_get_data.return_value = Mock()

        mock_get_data.return_value.json.return_value = mock_data
        mock_get_data.return_value.status_code = 200

        result = getdata()

        self.assertEqual(result,mock_data)


