from cognigy_client import Cognigy_client 

base_url = "http://api.cognigy.com"
api_key = "testapikey"
flow = "starwars"
reset_state = True
reset_context = True
username = "python-test-username"
channel = "python-test"

test = Cognigy_client(base_url, 3100, username, api_key, channel, flow)
test.connect()
print 'Connected'
test.send_message('Hi', None)
