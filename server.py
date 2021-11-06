from flask import Flask, request
import os
import json
import base64
import cv2
import numpy
from PIL import Image
from torch import Tensor
from torchvision import transforms

app = Flask(__name__)
app.debug = True


_RETURN_INVALID_REQUEST_PARAMETER = json.dumps({
    'Error': {
        'Code': 'SelectImage.InvalidRequestParameter',
                'Message': 'Invalid request parameter, check parameter'
    }
})

SELECT_IMAGE_PATH = None


@app.route("/")
def hello():
    return '<h1 style="color:blue">Hello...!</h1>'


@app.route('/select_image/', methods=['post'])
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
                'Code': 'SelectImage.ParameterError',
                'Message': 'parameter "file_name" not found in request'
            }
        })
    app.logger.info(data_json['file_name'])
    full_image_path=os.path.join('images',data_json['file_name'])
    app.logger.info(full_image_path)
    app.logger.info('select image %s in %s'%(data_json['file_name'],full_image_path))
    try:
        
        with open(full_image_path, 'rb') as f:
            image = base64.b64encode(f.read()).decode()
            
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

ROBUST_MODEL=None
TRANSFORM = transforms.Compose([transforms.Resize(224), transforms.ToTensor()])
from api_robustModel import RobustResnet34
@app.route('/robust_model/', methods=['post'])
def robust_model():
    app.logger.info("start /robust_model")
    """
        Parameter
        ---
            - `file_name` (str)
            - `topk` (int)
    """
    if not request.data:  # check if valid data
        return _RETURN_INVALID_REQUEST_PARAMETER

    # parase paramter
    data_get = request.data.decode('utf-8')
    data_json = json.loads(data_get)

    SELECT_IMAGE_PATH=os.path.join('images',data_json['file_name'])
    app.logger.info("select image: %s"%SELECT_IMAGE_PATH)
    image: numpy.ndarray = cv2.imread(SELECT_IMAGE_PATH)
    if image.shape[2] != 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_tensor: Tensor = TRANSFORM(Image.fromarray(image))
    
    try:
        ROBUST_MODEL=RobustResnet34(model_weight_path='api_robustModel/models/at_recon~lr=1e-4-best.pt', device='cpu')
    except:
        return json.dumps({
            'Error': {
                'Code': 'RobustModel.FileNotFound',
                'Message': 'error in load model'
            }
        })
    else:
        app.logger.info("successfully load model: %s"%ROBUST_MODEL)
    
    prob_list, index_list, name_list = ROBUST_MODEL.top_k(image_tensor, k=data_json['topk'])
    
    return json.dumps({
            'predict_name': name_list,
            'predict_prob': prob_list,
        })


if __name__ == '__main__':
    # app.run(host='192.168.1.141', port=2021)
    app.debug = True
    app.run(host='127.0.0.1', port=2021)
