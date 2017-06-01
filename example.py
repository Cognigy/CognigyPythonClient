from src.cognigy_client import Cognigy_client 

base_url = "http://api.cognigy.com"
api_key = "<your-api-key>"
flow = "<your-flow>"
reset_state = True
reset_context = True
username = "<your-username>"
channel = "<your-channel>"
language = "en-US"

def handle_output_method(result):
    print result

socket_client = Cognigy_client(base_url, 3100, username, api_key, channel, flow, language, handle_output=handle_output_method)
# has to connect first before sending message
socket_client.connect()
print 'Connected'
socket_client.send_message('Hi', None)
