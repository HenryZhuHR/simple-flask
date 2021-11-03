from flask import Flask, request, jsonify
import json

app = Flask(__name__)
app.debug = True


ERROR_POST_DATA_INVALID = 10
ERROR_IMAGE_INVALID = 11



@app.route('/', methods=['post'])
def add_stu():
    if not request.data:  # check if valid data
        return (ERROR_POST_DATA_INVALID)

    data_get = request.data.decode('utf-8')

    data_json = json.loads(data_get)  # 把区获取到的数据转为JSON格式
    print(data_json['command'])

    return 10


if __name__ == '__main__':
    app.run(host='192.168.1.141', port=2021)
