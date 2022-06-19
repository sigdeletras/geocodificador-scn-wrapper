import json
from dataclasses import dataclass
from urllib import request, parse
from urllib.error import URLError, HTTPError

API = 'https://geocoder-5-ign.larioja.org/v1/'


@dataclass
class GeocoderSCN:
    """Clase para almacenar los resultados de la RES API del Geocodificador del SCN"""
    search_text: str
    endpoint: str = None
    feature_count: int = 0
    api_data: str = None
    status: int = 0
    error: bool = False
    messages: str = None

    def search(self, api=API, layers='address', size=10):
        """
        Gocodificación directa.

        :param api: url API Geocodificador SCN
        :type api: str
        :param layers: Capas de datos a consultar, separados por comas. Por defecto address. Otros venue, street
        :type layers: str
        :param size: Número deseado de resultados. Por defecto 10
        :type size: int
        """
        self.endpoint = f'{API}/search?text={self.search_text}&layers={layers}&size={size}'

        text_parse = parse.quote_plus(self.search_text)
        url = f'{api}/search?text={text_parse}&layers={layers}&size={size}'

        try:
            with request.urlopen(url) as resp:
                self.status = resp.status
                self.api_data = json.loads(resp.read().decode('utf-8'))
                self.feature_count = len(self.api_data['features'])
                self.messages = "it's all OK!"

        except HTTPError as e:
            self.error = True
            self.status = e.code
            self.messages = e

        except URLError as e:
            self.error = True
            self.messages = e.reason

    def reverse(self, api=API, size=10):
        """
        Gocodificación indirecta.
        ej. https://geocoder-5-ign.larioja.org/v1/reverse?point.lat=40.416645598&point.lon=-3.70381211
        :param api: url API Geocodificador SCN
        :type api: str
        :param size: Número deseado de resultados. Por defecto 10
        :type size: int
        """
        coor = self.search_text.strip().split(',')

        try:
            lat = coor[0]
            lon = coor[1]
        except IndexError as e:
            self.error = True
            self.messages = f'IndexError. Bad coordinates in {self.search_text}'
            return

        self.endpoint = f'{API}reverse?point.lat={lat}&point.lon={lon}&size={size}'

        try:
            with request.urlopen(self.endpoint) as resp:
                self.status = resp.status
                self.api_data = json.loads(resp.read().decode('utf-8'))
                self.feature_count = len(self.api_data['features'])
                self.messages = "it's all OK!"

        except HTTPError as e:
            self.error = True
            self.status = e.code
            self.messages = e

        except URLError as e:
            self.error = True
            self.messages = e.reason

    def get_list(self):
        """
        Devuelve una lista con lonfitud, latitud, etiquea y fuente de la geocodifiación
        @rtype: object
        """
        list = []
        if self.feature_count > 0:
            features = self.api_data['features']
            i = 1
            for f in features:
                dic = {
                    'id': i,
                    'lon': f['geometry']['coordinates'][0],
                    'lat': f['geometry']['coordinates'][1],
                    'label': f['properties']['label'],
                    'source': f['properties']['source'],
                }
                list.append(dic)
                i += 1
        return list
