from cognigy_client import Cognigy_client 

base_url = "http://api.cognigy.com:3100"
api_key = "testapikey"
flow = "starwars"
reset_state = True
reset_context = True
username = "test-username"
channel = "python-test"

test = Cognigy_client(base_url, username, api_key, channel, flow)
test.connect()
test.send_message('test', None)
