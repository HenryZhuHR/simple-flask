import json
from flask.wrappers import Response
import requests

import base64
with open('adv_100001.png', 'rb') as f:
    image = base64.b64encode(f.read()).decode()

# url = 'http://192.168.1.141:2021/select_image/'
# url = 'http://127.0.0.1:2021/select_image/'
url = 'http://1.116.121.100/select_image/'
# url = 'http://202.114.107.172/select_image/'



response = requests.post(url, data=json.dumps({
    'image': 'adv_100001.png'
}))
print(response)
if 'Error' in response.json():
    print('error')


data = {
    'file_name': 'adv_100001.png'
}
response = requests.post(url, data=json.dumps(data))
if 'Error' in response.json():
    print('error:')
    print(response.json()['Error'])
else:
    image_data = base64.b64decode(response.json()['image'])
    with open('getImage.jpg','wb') as f_img:
        f_img.write(image_data)
