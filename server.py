from flask import Flask, request
from flask import render_template  # 渲染
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


from flask_cors import CORS

from api.api_robustModel import RobustResnet34
from api.api_originalModel import OriginalModel
from api.api_recon.recon import Recon
from api.api_detect.detect import Detect

app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')
app.debug = True
CORS(app, resources={r"/api/*": {"origins": "*"}})

_RETURN_INVALID_REQUEST_PARAMETER = json.dumps({
    'Error': {
        'Code': 'NotParameterGet',
                'Message': 'Invalid request parameter got, check parameter'
    }
})

SELECT_IMAGE = None
RECON_IMAGE_TENSOR = None


ORIGINAL_MODEL_PATH = 'api/api_originalModel/models/resnet34.pt'
ORIGINAL_MODEL = OriginalModel(model_weight_path=ORIGINAL_MODEL_PATH,
                               device='cpu')
ROBUST_MODEL_PATH = 'api/api_robustModel/models/at_recon~lr=1e-4-best.pt'
ROBUST_MODEL = RobustResnet34(model_weight_path=ROBUST_MODEL_PATH,
                              device='cpu')
RECON_MODEL_PATH = './api/api_recon/recon_model.pt'
RECON_MODEL = Recon(
    model_path=RECON_MODEL_PATH, device='cpu')
TRANSFORM = transforms.Compose(
    [transforms.Resize(224), transforms.ToTensor()])


@app.route("/")
def hello():
    # return render_template('index.html')
    return 'hello-1110'


@app.route('/api/upload_image', methods=['post'])
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
            'status': 'Success'
        })
    except:
        return json.dumps({
            'Error': {
                'Code': 'UploadImage.DecodeImageError',
                'Message': 'decode image error'
            }
        })


@app.route('/api/original_model', methods=['post'])
def original_model():
    """
        Parameter
        ---
    """
    global SELECT_IMAGE
    global ORIGINAL_MODEL
    global TRANSFORM

    try:
        image: numpy.ndarray = cv2.cvtColor(
            np.asarray(Image.open(io.BytesIO(SELECT_IMAGE))), cv2.COLOR_RGB2BGR)
        # cv2.imwrite('source/save.jpg', image)
    except:
        return json.dumps({
            'Error': {
                'Code': 'OriginalModel.NotImage',
                'Message': 'not select or upload image'
            }
        })

    if image.shape[2] != 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image_tensor: Tensor = TRANSFORM(Image.fromarray(image))

    if ORIGINAL_MODEL is None:
        try:
            app.logger.info('Original Model path: %s' % ORIGINAL_MODEL_PATH)
            ORIGINAL_MODEL = OriginalModel(
                model_weight_path=ORIGINAL_MODEL_PATH,
                device='cpu')
        except:
            return json.dumps({
                'Error': {
                    'Code': 'OriginalModel.FileNotFound',
                    'Message': 'error in load model'
                }
            })
        else:
            app.logger.info('successfully load model: %s' %
                            ORIGINAL_MODEL_PATH)

    topk = 10
    app.logger.info(ORIGINAL_MODEL)
    prob_list, index_list, name_list = ORIGINAL_MODEL.top_k(
        image_tensor, k=topk)

    return json.dumps({
        'image': base64.b64encode(SELECT_IMAGE).decode(),
        'predict': {name_list[i]: prob_list[i] for i in range(topk)}
    })


@app.route('/api/robust_model', methods=['post'])
def robust_model():
    """
        Parameter
        ---
    """
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

    if ROBUST_MODEL is None:
        try:
            app.logger.info('Robust Model path: %s' % ROBUST_MODEL_PATH)
            ROBUST_MODEL = RobustResnet34(
                model_weight_path=ROBUST_MODEL_PATH,
                device='cpu')
        except:
            return json.dumps({
                'Error': {
                    'Code': 'RobustModel.ModelError',
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


@app.route('/api/reconstructed_model', methods=['post'])
def reconstructed_model():
    """
        Parameter
        ---
    """
    global RECON_IMAGE_TENSOR
    global RECON_MODEL_PATH
    global RECON_MODEL


    if RECON_MODEL is None:
        try:
            app.logger.info('recon Model path: %s' % RECON_MODEL_PATH)
            RECON_MODEL = Recon(model_path=RECON_MODEL_PATH, device='cpu')
        except:
            return json.dumps({
                'Error': {
                    'Code': 'ReconstructedModel.ModelError',
                    'Message': 'error in load model'
                }
            })
        else:
            app.logger.info('successfully load model: %s' % RECON_MODEL_PATH)
        

    try:
        image: numpy.ndarray = cv2.cvtColor(
            np.asarray(Image.open(io.BytesIO(SELECT_IMAGE))), cv2.COLOR_RGB2BGR)
        # cv2.imwrite('source/save.jpg', image)
    except:
        return json.dumps({
            'Error': {
                'Code': 'ReconstructedModel.NotImage',
                'Message': 'not select or upload image'
            }
        })

    if image.shape[2] != 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image_tensor: Tensor = TRANSFORM(Image.fromarray(image))
    image_recon: Tensor = RECON_MODEL.recon(image_in=image_tensor)
    RECON_IMAGE_TENSOR = image_recon

    image_recon_np: numpy.ndarray = image_recon.detach().numpy()*255
    image_recon_np = np.squeeze(image_recon_np)
    image_recon_np = np.transpose(image_recon_np, (1, 2, 0))
    image_recon_np = cv2.cvtColor(image_recon_np, cv2.COLOR_RGB2BGR)

    cv2.imwrite("static/image_recon.jpg", image_recon_np)

    with open("static/image_recon.jpg", 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode()

    return json.dumps({
        "image": image_base64
    })


@app.route('/api/adversarial_detect', methods=['post'])
def adversarial_detect():
    """
        Parameter
        ---
    """
    global SELECT_IMAGE
    try:
        image: numpy.ndarray = cv2.cvtColor(
            np.asarray(Image.open(io.BytesIO(SELECT_IMAGE))), cv2.COLOR_RGB2BGR)
        # cv2.imwrite('source/save.jpg', image)
    except:
        return json.dumps({
            'Error': {
                'Code': 'AdversarialDetect.NotImage',
                'Message': 'not select or upload image'
            }
        })

    if image.shape[2] != 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image_tensor: Tensor = TRANSFORM(Image.fromarray(image))

    is_AE, probability, threshold = Detect(
        model_path='api/api_detect/Detect.pkl',
        device='cpu',
        image_tensor=image_tensor,
        thre=0.8).detect()

    return json.dumps({
        "is_adversarialExample": is_AE,
        "probability": probability,
        "threshold": threshold,
    })


if __name__ == '__main__':

    # app.run(host='192.168.1.141', port=2021)
    app.run(host='127.0.0.1', port=2021)
