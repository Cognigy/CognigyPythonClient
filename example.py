from src.cognigy_client import Cognigy_client 

base_url = "http://api.cognigy.com"
api_key = "testapikey"
flow = "starwars"
reset_state = True
reset_context = True
username = "python-test-username"
channel = "python-test"
language = "en-US"

def handle_output_method(result):
    print 'lalalala'
    print result

test = Cognigy_client(base_url, 3100, username, api_key, channel, flow, language, handle_output=handle_output_method)
test.connect()
print 'Connected'
test.send_message('Hi', None)
