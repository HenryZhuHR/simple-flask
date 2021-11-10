"""
for run :

pip3 install requests
pip3 flask requests
"""

from pprint import pprint
import json
from flask.wrappers import Response
import requests

import base64

# URL_BASE = 'http://1.116.121.100/api'
URL_BASE = 'http://127.0.0.1:2021/api'



# Test upload_image
url = '%s/upload_image' % URL_BASE
image_path='source/images/automobile_0002.jpg'
data = {
    'image': base64.b64encode(open(image_path, 'rb').read()).decode()
}
response = requests.post(url, data=json.dumps(data))
pprint(response.json())



# Test original_model
url = '%s/original_model' % URL_BASE
response = requests.post(url, data=json.dumps({}))
pprint(response.json()['predict'])

# Test robust_model
url = '%s/robust_model' % URL_BASE
response = requests.post(url, data=json.dumps({}))
pprint(response.json()['predict'])

# Test reconstructed_model
url = '%s/reconstructed_model' % URL_BASE
response = requests.post(url, data=json.dumps({}))
pprint(response.json())

# Test adversarial_detect
url = '%s/adversarial_detect' % URL_BASE
response = requests.post(url, data=json.dumps({}))
pprint(response.json())

