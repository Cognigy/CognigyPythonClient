from socketIO_client import SocketIO, LoggingNamespace
import logging
import requests
import json
import sys

# logger
import logging
import Colorer
logging.basicConfig(level=logging.DEBUG)

class Cognigy_client:

    def __init__(self, socket_host, socket_port,
                 user, api_key, channel, flow, **kwargs):
        self.socket_host = socket_host
        self.socket_port = socket_port
        self.token = None
        self.socket_io = None

        self.options_user = user
        self.options_api_key = api_key
        self.options_channel = channel
        self.options_flow = flow
        self.options_token = kwargs.get('token', None)

    @staticmethod
    def on_connect():
        print 'Connected!'

    @staticmethod
    def on_disconnect():
        print 'Disconnected!'

    @staticmethod
    def on_output(*args):
        print 'Output detected'
        print('output', args)
    
    @staticmethod
    def on_error(*args):
        for arg in args:
            logging.error(arg)

    def connect(self):
        self.token = self.__get_token()

        self.socket_io = SocketIO(self.socket_host, self.socket_port, params={'token': self.token})

        self.socket_io.on('output', self.on_output)
        self.socket_io.on('connect', self.on_connect)
        self.socket_io.on('error', self.on_error)
        self.socket_io.on('exception', self.on_error)
        self.socket_io.on('disconnect', self.on_disconnect)
        print 'Events setup finished'
        self.socket_io.wait(10)

    def send_message(self, message, data):
        print 'Sending message: ' + message
        self.socket_io.emit('input', {"text": message, "data": data})
        self.socket_io.wait(10)

    def __get_token(self):
        url = '{0}:{1}/loginDevice'.format(self.socket_host, self.socket_port)
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        json_data = {
            "user": self.options_user,
            "channel": self.options_channel,
            "apikey": self.options_api_key
        }

        token_response = requests.post(url, json=json_data, headers=headers).json()
        print 'TOKEN RESPONSE :' + token_response['token']

        if token_response is None:
            print 'No token detected'
            return None

        return token_response['token']
