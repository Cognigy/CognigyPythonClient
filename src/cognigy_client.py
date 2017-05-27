from socketIO_client import SocketIO, LoggingNamespace
import requests
import sys
import json

import logging
import src.Colorer
FORMATTER = '%(asctime)s - [Python Client - %(funcName)s] - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMATTER)

class CognigyClient(object):

    """Cognigy python client"""

    def __init__(self, socket_host, socket_port,
                 user, api_key, channel, flow, language, **kwargs):

        self.logger = logging.getLogger(__name__)

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
        self.options_reset_flow = kwargs.get('reset_flow', False)
        if self.options_reset_flow is None and not isinstance(self.options_reset_flow, bool):
            self.options_reset_flow = False

        self.options_reset_state = kwargs.get('reset_state', False)
        if self.options_reset_state is None and not isinstance(self.options_reset_state, bool):
            self.options_reset_state = False

        self.options_reset_context = kwargs.get('reset_context', False)
        if self.options_reset_context is None and not isinstance(self.options_reset_context, bool):
            self.options_reset_context = False

        # set optional values
        self.options_keep_markup = kwargs.get('keep_markup', False)
        if self.options_keep_markup is None and not isinstance(self.options_keep_markup, bool):
            self.options_keep_markup = False

        self.handle_output = kwargs.get('handle_output', None)

    def on_connect(self):
        """Do on connected"""
        self.logger.info('Connected!')

    def on_disconnect(self):
        """Do on disconnected"""
        self.logger.info('Disconnected!')

    def on_error(self, *args):
        """On receiving error from Cognigy brain"""
        for arg in args:
            self.logger.error(arg)

    def on_output(self, *args):
        """Process output from Cognigy brain"""
        self.logger.debug('Output detected: {0}'.format(args[0]))
        result = args[0]
        if self.options_keep_markup:
            result["text"] = result["text"].replace(r"<[^>]*>", "")
        if self.handle_output:
            self.handle_output(result)

    def connect(self):
        """Connect to Cognigy brain"""
        try:
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
                "resetState": self.options_reset_state,
                "resetContext": self.options_reset_context
            })

            self.socket_io.on('output', self.on_output)
            self.socket_io.on('connect', self.on_connect)
            self.socket_io.on('error', self.on_error)
            self.socket_io.on('exception', self.on_error)
            self.socket_io.on('disconnect', self.on_disconnect)

            self.logger.debug('Events setup finished')
            self.socket_io.wait(10)

        except:
            self.logger.error(sys.exc_info()[0])
            self.logger.error("Error on initiating socket connection, please check if you're using the right API key")

    def send_message(self, message, data):
        """Send message to brain"""
        self.logger.info('Sending message: ' + message)
        self.socket_io.emit('input', {"text": message, "data": data})
        self.socket_io.wait(10)

    def reset_flow(self, new_flow_id, language, version):
        """Change to another flow"""
        self.socket_io.emit('resetFlow', {
            "id": new_flow_id,
            "language": language,
            "version": version})
        self.socket_io.wait(10)

    def reset_state(self):
        """Reset current flow state"""
        self.socket_io.emit('resetState')
        self.socket_io.wait(10)

    def inject_state(self, state):
        """Send an inject state event"""
        if not isinstance(state, str):
            self.logger.error('State is not a string, please use only string as state')

        self.socket_io.emit('injectState', state)
        self.socket_io.wait(10)

    def inject_context(self, context):
        """Send an inject state event"""
        try:
            json_context = json.loads(context)
            self.socket_io.emit('injectContext', json_context)
            self.socket_io.wait(10)

        except ValueError:
            self.logger.error('Context object is not JSON, please only use JSON object')

    def set_event_handler(self, event, handler):
        """Manual socket io event handling"""
        self.socket_io.on(event, handler)
        self.socket_io.wait(10)

    def __get_token(self):
        """Private function to get token for connecting"""
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
