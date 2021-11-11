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

URL_BASE = 'http://1.116.121.100/api'
# URL_BASE = 'http://127.0.0.1:2021/api'



# Test upload_image
url = '%s/upload_image' % URL_BASE
image_path='source/images/adv_100601.png'
data = {
    'image': base64.b64encode(open(image_path, 'rb').read()).decode()
}
response = requests.post(url, data=json.dumps(data))
pprint(response.json())

# ============================================================
#       original_image
# ============================================================
# Test original_model
url = '%s/original_model' % URL_BASE
data = {
    'mode': 'original_image'
}
print()
print('-- /api/original_model + mode:original_image')
response = requests.post(url, data=json.dumps(data))
print(response.json()['predict'])

# Test robust_model
url = '%s/robust_model' % URL_BASE
data = {
    'mode': 'original_image'
}
response = requests.post(url, data=json.dumps(data))
print()
print('-- /api/robust_model + mode:original_image')
print(response.json()['predict'])

# Test adversarial_detect
url = '%s/adversarial_detect' % URL_BASE
data = {
    'mode': 'original_image'
}
print()
print('-- /api/adversarial_detect + mode:original_image')
response = requests.post(url, data=json.dumps(data))
print(response.json())



# ============================================================
#       Test original_model without /api/reconstructed_model
# ============================================================

# Test original_model without /api/reconstructed_model
url = '%s/original_model' % URL_BASE
data = {
    'mode': 'reconstructed_image'
}
print()
print('-- /api/original_model + mode:original_image')
response = requests.post(url, data=json.dumps(data))
pprint(response.json())

# ============================================================
#       After reconstructed_model
# ============================================================

# Test reconstructed_model
url = '%s/reconstructed_model' % URL_BASE
data = {
    'mode': 'reconstructed_image'
}
response = requests.post(url, data=json.dumps(data))
print()
print('-- /api/reconstructed_model')
print(response.json()['image'][:10])

# Test original_model
url = '%s/original_model' % URL_BASE
data = {
    'mode': 'reconstructed_image'
}
response = requests.post(url, data=json.dumps(data))
print()
print('-- /api/original_model + mode:reconstructed_image')
print(response.json()['predict'])

# Test robust_model
url = '%s/robust_model' % URL_BASE
data = {
    'mode': 'reconstructed_image'
}
response = requests.post(url, data=json.dumps(data))
print()
print('-- /api/robust_model + mode:reconstructed_image')
print(response.json()['predict'])

# Test adversarial_detect
url = '%s/adversarial_detect' % URL_BASE
data = {
    'mode': 'reconstructed_image'
}
response = requests.post(url, data=json.dumps(data))
print()
print('-- /api/adversarial_detect + mode:reconstructed_image')
print(response.json())


# ============================================================
#       Test physics_worldl
# ============================================================

# Test physics_world
url = '%s/physics_world' % URL_BASE
import time
st=time.time()
response = requests.post(url, data=json.dumps({}))
et=time.time()
print()
print('-- /api/physics_world')
pprint(response.json()['image'])
pprint(response.json()['predict'])
print(et-st)

