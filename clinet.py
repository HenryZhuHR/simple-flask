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

URL_BASE = 'http://1.116.121.100'
URL_BASE = 'http://127.0.0.1:2021'

# Test select_image
url = '%s/select_image' % URL_BASE
data = {
    'file_name': 'adv_100601.png'
}
"""
Available files:
    adv_100401.png
    adv_100601.png
    adv_100801.png
    adv_101201.png
    adv_101402.png
    adv_101802.png
"""
response = requests.post(url, data=json.dumps(data))
if 'Error' in response.json():
    print('error:')
    print(response.json()['Error'])
else:
    image_data = base64.b64decode(response.json()['image'])
    with open('getImage.jpg', 'wb') as f_img:
        f_img.write(image_data)
print()


# Test upload_image
url = '%s/upload_image' % URL_BASE
image_path='images/adv_100601.png'
data = {
    'image': base64.b64encode(open(image_path, 'rb').read()).decode()
}
response = requests.post(url, data=json.dumps(data))
pprint(response.json())



# Test robust_model
url = '%s/robust_model' % URL_BASE
response = requests.post(url, data=json.dumps({}))
pprint(response.json()['predict'])


