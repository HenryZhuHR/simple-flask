from flask import Flask, request
from flask import render_template #渲染
import os
import io
import json
import base64
import cv2
import numpy
import numpy as np
from PIL import Image
from torch import Tensor
from torchvision import transforms
from api.api_robustModel import RobustResnet34


app = Flask(__name__)
app.debug = True


_RETURN_INVALID_REQUEST_PARAMETER = json.dumps({
    'Error': {
        'Code': 'NotParameterGet',
                'Message': 'Invalid request parameter got, check parameter'
    }
})

SELECT_IMAGE = None


ROBUST_MODEL = None  # for robust_model()
ROBUST_MODEL_PATH = 'api/api_robustModel/models/at_recon~lr=1e-4-best.pt'
TRANSFORM = transforms.Compose(  # for robust_model()
    [transforms.Resize(224), transforms.ToTensor()])


@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/select_image', methods=['post'])
def select_image():
    """
        Parameter
        ---
            - `file_name` (str)
    """
    if not request.data:  # check if valid data
        return _RETURN_INVALID_REQUEST_PARAMETER

    # parase paramter
    data_get = request.data.decode('utf-8')
    data_json = json.loads(data_get)

    if 'file_name' not in data_json:
        return json.dumps({
            'Error': {
                'Code': 'SelectImage.LossParameter',
                'Message': 'parameter "file_name" not found in request'
            }
        })

    global SELECT_IMAGE
    image_file = os.path.join('source','images', data_json['file_name'])
    app.logger.info('/select_image :select image %s in %s' %
                    (data_json['file_name'], image_file))
    try:

        with open(image_file, 'rb') as f:
            SELECT_IMAGE = f.read()
            image = base64.b64encode(SELECT_IMAGE).decode()

        return json.dumps({
            'image': image
        })
    except:
        return json.dumps({
            'Error': {
                'Code': 'SelectImage.FileNotFound',
                'Message': 'request image file %s not found' % data_json['file_name']
            }
        })


@app.route('/upload_image', methods=['post'])
def upload_image():
    """
        Parameter
        ---
            - `image` (base64)
    """
    if not request.data:  # check if valid data
        return _RETURN_INVALID_REQUEST_PARAMETER
    # parase paramter
    data_json = json.loads(request.data.decode('utf-8'))
    if 'image' not in data_json:
        return json.dumps({
            'Error': {
                'Code': 'UploadImage.LossParameter',
                'Message': 'parameter "image" not found in request'
            }
        })

    global SELECT_IMAGE

    try:
        image_data = base64.b64decode(data_json['image'])
        SELECT_IMAGE = image_data
        with open('source/default.jpg', 'wb') as f_img:
            f_img.write(SELECT_IMAGE)
        return json.dumps({
            'statement': 'Success'
        })
    except:
        return json.dumps({
            'Error': {
                'Code': 'UploadImage.DecodeImageError',
                'Message': 'decode image error'
            }
        })


@app.route('/robust_model', methods=['post'])
def robust_model():
    """
        Parameter
        ---
    """
    if not request.data:  # check if valid data
        return _RETURN_INVALID_REQUEST_PARAMETER

    # parase paramter
    data_json = json.loads(request.data.decode('utf-8'))

    global SELECT_IMAGE
    global ROBUST_MODEL
    global TRANSFORM

    try:
        image: numpy.ndarray = cv2.cvtColor(
            np.asarray(Image.open(io.BytesIO(SELECT_IMAGE))), cv2.COLOR_RGB2BGR)
        # cv2.imwrite('source/save.jpg', image)
    except:
        return json.dumps({
            'Error': {
                'Code': 'RobustModel.NotImage',
                'Message': 'not select or upload image'
            }
        })

    if image.shape[2] != 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image_tensor: Tensor = TRANSFORM(Image.fromarray(image))

    try:
        app.logger.info('Robust Model path: %s'%ROBUST_MODEL_PATH)
        ROBUST_MODEL = RobustResnet34(
            model_weight_path=ROBUST_MODEL_PATH, 
            device='cpu')
    except:
        return json.dumps({
            'Error': {
                'Code': 'RobustModel.FileNotFound',
                'Message': 'error in load model'
            }
        })
    else:
        app.logger.info('successfully load model: %s' % ROBUST_MODEL)

    topk = 10
    prob_list, index_list, name_list = ROBUST_MODEL.top_k(image_tensor, k=topk)

    return json.dumps({
        'image': base64.b64encode(SELECT_IMAGE).decode(),
        'predict': {name_list[i]: prob_list[i] for i in range(topk)}
    })


if __name__ == '__main__':
    # app.run(host='192.168.1.141', port=2021)
    app.run(host='127.0.0.1', port=2021)
