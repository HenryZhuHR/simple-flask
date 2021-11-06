"""
for run :

pip3 install requests
pip3 flask requests
"""

import json
from flask.wrappers import Response
import requests

import base64

URL_BASE='http://1.116.121.100'
# URL_BASE='http://127.0.0.1:2021'


url = '%s/select_image/'%URL_BASE
data = {
    'file_name': 'adv_101802.png'
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
    with open('getImage.jpg','wb') as f_img:
        f_img.write(image_data)
        print(' [INFO] Image get from server write to getImage.jpg')
print()

data['topk'] = 10
url = '%s/robust_model/'%URL_BASE
response = requests.post(url, data=json.dumps(data))
from pprint import pprint
pprint(response.json())