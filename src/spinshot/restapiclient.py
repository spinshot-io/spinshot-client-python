import logging
from pathlib import Path
import configparser

import requests

LOGGER = logging.getLogger(__name__)


class RestApiException(Exception):
    def __init__(self, message):
        super().__init__(message)


class RestAPIClient:
    def __init__(self, secret_key=None, host=None, port=None, use_ssl=None):
        self.secret_key = secret_key
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.__config()

    def __config(self):
        SETTINGS_INI = (
            Path.home() / '.spinshot' / 'config',
            Path('/etc/spinshot/config')
        )

        config = configparser.ConfigParser()

        for config_file in SETTINGS_INI:
            if config_file.exists():
                config.read(config_file)

                if self.host is None and config.has_option('default', 'host'):
                    self.host = config.get('default', 'host')

                if self.port is None and config.has_option('default', 'port'):
                    self.port = config.get('default', 'port')

                if self.use_ssl is None and config.has_option('default', 'use_ssl'):
                    value = config.get('default', 'use_ssl').lower()
                    self.use_ssl = True if value in ('yes', 'true') else False

                if self.secret_key is None and config.has_option('default', 'secret_key'):
                    self.secret_key = config.get('default', 'secret_key')

        if self.host is None:
            self.host = 'api.spinshot.io'

        if self.use_ssl is None:
            self.use_ssl = True

        if self.port is None:
            if self.use_ssl is True:
                self.port = 443
            else:
                self.port = 80

    @property
    def _proto(self):
        return 'https' if self.use_ssl else 'http'

    def _headers(self):
        return {
            'authorization': f'Api-Key {self.secret_key}'
        }

    def list(self, endpoint, params={}):
        url = f'{self._proto}://{self.host}:{self.port}/{endpoint}/'

        try:
            response = requests.get(url, headers=self._headers(), params=params)
        except Exception as e:
            raise RestApiException(e)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 400:
            raise RestApiException(response.text)

        if response.status_code == 403:
            raise RestApiException('authorization error')

        raise RestApiException("Unexpected status code: {}".format(response.status_code))

    def retrieve(self, endpoint, pk):
        url = f'{self._proto}://{self.host}:{self.port}/{endpoint}/{pk}/'

        try:
            response = requests.get(url, headers=self._headers())
        except Exception as e:
            raise RestApiException(e)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 400:
            raise RestApiException(response.text)

        if response.status_code == 403:
            raise RestApiException('authorization error')

        raise RestApiException("Unexpected status code: {}".format(response.status_code))

    def create(self, endpoint, instance):
        url = f'{self._proto}://{self.host}:{self.port}/{endpoint}/'

        try:
            json = instance.create_json()
            if 'files' in json:
                files = json['files']
                del json['files']
                response = requests.post(url, data=json, files=files, headers=self._headers())
            else:
                response = requests.post(url, json=json, headers=self._headers())

        except Exception as e:
            raise RestApiException(e)

        if response.status_code == 201:
            return response.json()

        if response.status_code == 400:
            raise RestApiException(response.text)

        if response.status_code == 403:
            raise RestApiException('authorization error')

        with open('/Users/christian/error.html', 'wb') as fh:
            fh.write(response.content)

        raise RestApiException(f"Unexpected status code: {response.status_code}")

    def update(self, endpoint, instance):
        url = f'{self._proto}://{self.host}:{self.port}/{endpoint}/{instance.uid}/'

        try:
            json = instance.update_json()
            if 'files' in json:
                files = json['files']
                del json['files']
                response = requests.post(url, data=json, files=files, headers=self._headers())
            else:
                response = requests.patch(url, json=json, headers=self._headers())
        except Exception as e:
            raise RestApiException(e)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 400:
            raise RestApiException(response.text)

        if response.status_code == 403:
            raise RestApiException('authorization error')

        raise RestApiException("Unexpected status code: {}".format(response.status_code))

    def delete(self, endpoint, instance):
        url = f'{self._proto}://{self.host}:{self.port}/{endpoint}/{instance.uid}/'

        try:
            response = requests.delete(url, headers=self._headers())
        except Exception as e:
            raise RestApiException(e)

        if response.status_code == 204:
            return True

        if response.status_code == 403:
            raise RestApiException('authorization error')

        raise RestApiException("Unexpected status code: {}".format(response.status_code))
