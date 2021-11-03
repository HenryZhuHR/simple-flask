import json
import requests

import base64
with open('adv_100001.png', 'rb') as f:
    image = base64.b64encode(f.read()).decode()

data = {
    'command': 'robustModel',
    'image':image
}
url = 'http://192.168.1.141:2021/'

r = requests.post(url, data=json.dumps(data))
print(r.json()['command'])
