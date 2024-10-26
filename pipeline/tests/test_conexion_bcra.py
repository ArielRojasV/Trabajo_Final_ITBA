from unittest import TestCase
from unittest.mock import patch   
import requests


def url_exists(url):
    r = requests.get(url)
    if r.status_code == 200:
        return True
    elif r.status_code == 404:
        return False

# Test para ver si url responde
class Test_Get_Data(TestCase):
    def test_return_true(self):
        with patch('requests.get') as mock_request:
            url = "https://api.bcra.gob.ar/" 

            mock_request.return_value.status_code = 200

            self.assertTrue(url_exists(url))

            mock_request.assert_called_once_with(url)

 