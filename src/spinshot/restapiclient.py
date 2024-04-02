import logging
from pathlib import Path
import configparser

import requests

LOGGER = logging.getLogger(__name__)


class RestApiException(Exception):
    def __init__(self, message):
        super().__init__(message)


class RestAPIClient:
    def __init__(self, config=None):
        self.host = 'api.spinshot.io'
        self.port = 443
        self.use_ssl = True
        self.proto = 'https'
        self.secret_key = None

        if config is None:
            self.config_files = (
                Path.home() / '.spinshot' / 'config',
                Path('/etc/spinshot/config')
            )
        else:
            self.config_files = [
                Path(config)
            ]

        self.configure()

    def configure(self):
        configured = False
        for config_file in self.config_files:
            if config_file.exists():
                self.read_config_file(config_file)
                configured = True

        if configured == False:
            raise RestApiException('config missing')

        if self.secret_key is None:
            raise RestApiException('config has no secret key')

    def read_config_file(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        if config.has_option('default', 'host'):
            self.host = config.get('default', 'host')

        if config.has_option('default', 'port'):
            self.port = config.get('default', 'port')

        if config.has_option('default', 'use_ssl'):
            value = config.get('default', 'use_ssl').lower()
            self.use_ssl = True if value in ('yes', 'true') else False
            if self.use_ssl in ('yes', 'true'):
                self.proto = 'https'
            else:
                self.proto = 'http'

        if config.has_option('default', 'secret_key'):
            self.secret_key = config.get('default', 'secret_key')

    def _headers(self):
        return {
            'authorization': f'Api-Key {self.secret_key}'
        }

    def list(self, endpoint, params={}):
        url = f'{self.proto}://{self.host}:{self.port}/{endpoint}/'

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
        url = f'{self.proto}://{self.host}:{self.port}/{endpoint}/{pk}/'

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
        url = f'{self.proto}://{self.host}:{self.port}/{endpoint}/'

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
        url = f'{self.proto}://{self.host}:{self.port}/{endpoint}/{instance.uid}/'

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
        url = f'{self.proto}://{self.host}:{self.port}/{endpoint}/{instance.uid}/'

        try:
            response = requests.delete(url, headers=self._headers())
        except Exception as e:
            raise RestApiException(e)

        if response.status_code == 204:
            return True

        if response.status_code == 403:
            raise RestApiException('authorization error')

        raise RestApiException("Unexpected status code: {}".format(response.status_code))
