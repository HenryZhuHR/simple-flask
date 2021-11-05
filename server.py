from flask import Flask, request
import json
import base64

app = Flask(__name__)
app.debug = True


_RETURN_INVALID_REQUEST_PARAMETER = json.dumps({
    'Error': {
        'Code': 'SelectImage.InvalidRequestParameter',
                'Message': 'Invalid request parameter, check parameter'
    }
})


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

    try:
        with open(data_json['file_name'], 'rb') as f:
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

@app.route('/robust_model/', methods=['post'])
def robust_model():
    pass


if __name__ == '__main__':
    app.run(host='192.168.1.141', port=2021)
