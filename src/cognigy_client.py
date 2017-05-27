from socketIO_client import SocketIO, LoggingNamespace
import requests

import logging
import src.Colorer
logging.basicConfig(level=logging.INFO)

class Cognigy_client:

    def __init__(self, socket_host, socket_port,
                 user, api_key, channel, flow, language, **kwargs):

        self.logger = logger = logging.getLogger(__name__)

        self.socket_host = socket_host
        self.socket_port = socket_port
        self.token = None
        self.socket_io = None

        self.options_user = user
        self.options_api_key = api_key
        self.options_channel = channel
        self.options_flow = flow
        self.options_language = language
        self.options_token = kwargs.get('token', None)
        self.option_version = kwargs.get('version', None)
        self.options_passthrough_ip = kwargs.get('passthrough_ip', None)

        # reset state, context, flow
        self.reset_flow = kwargs.get('reset_flow', None)
        if self.reset_flow is None and not isinstance(self.reset_flow, bool):
            self.reset_flow = False
        
        self.reset_state = kwargs.get('reset_state', None)
        if self.reset_state is None and not isinstance(self.reset_state, bool):
            self.reset_state = False

        self.reset_context = kwargs.get('reset_context', None)
        if self.reset_context is None and not isinstance(self.reset_context, bool):
            self.reset_context = False

        self.options_keep_markup = kwargs.get('keep_markup', None)
        if self.options_keep_markup is None and not isinstance(self.options_keep_markup, bool):
            self.options_keep_markup = False
        
        self.handle_output = kwargs.get('handle_output', None)

    def on_connect(self):
        self.logger.info('Connected!')

    def on_disconnect(self):
        self.logger.info('Disconnected!')

    def on_error(self, *args):
        for arg in args:
            self.logger.error(arg)

    def on_output(self, *args):
        self.logger.debug('Output detected: {0}'.format(args[0]))
        result = args[0]
        if self.options_keep_markup:
            result["text"] = result["text"].replace(r"<[^>]*>", "")
        if self.handle_output:
            self.handle_output(result)

    def connect(self):
        self.token = self.__get_token()

        self.socket_io = SocketIO(self.socket_host, self.socket_port, params={'token': self.token})

        # init first before start sending message
        self.logger.info('Initializing connection')
        self.socket_io.emit("init", {
					       "flowId": self.options_flow,
					       "language": self.options_language,
					       "version": self.option_version,
            "passthroughIP": self.options_passthrough_ip,
            "resetFlow": self.reset_flow,
            "resetState": self.reset_state,
            "resetContext": self.reset_context
        })

        self.socket_io.on('output', self.on_output)
        self.socket_io.on('connect', self.on_connect)
        self.socket_io.on('error', self.on_error)
        self.socket_io.on('exception', self.on_error)
        self.socket_io.on('disconnect', self.on_disconnect)
        
        self.logger.debug('Events setup finished')
        self.socket_io.wait(10)

    def send_message(self, message, data):
        self.logger.info('Sending message: ' + message)
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
        self.logger.debug('TOKEN RESPONSE :' + token_response['token'])

        if token_response is None:
            self.logger.error('No token detected')
            return None

        return token_response['token']
