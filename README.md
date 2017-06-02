# Cognigy Python Client
Repo for the cognigy (server) client which can be used 
to connect to the cognigy brain from server applications.

## Installation
Clone the git folder and the python client code is in src folder

## Usage
Below is the example on how to use the python class.
The same code is in example.py.

```python
from src.cognigy_client import CognigyClient 

base_url = "http://api.cognigy.com"
port = 3100
api_key = "<your-api-key>"
flow = "<your-flow>"
reset_state = True
reset_context = True
username = "<your-user>"
channel = "<your-channel>"
language = "en-US"

def handle_output_method(result):
    print(str(result))

socket_client = CognigyClient(base_url, port, username, api_key, channel, flow, language, handle_output=handle_output_method)
# has to connect first before sending message
socket_client.connect()
print('Connected')
socket_client.send_message('Hi', None)
```
