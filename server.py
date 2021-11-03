from flask import Flask, request, jsonify
import json

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['post'])
def add_stu():
    if not request.data:  # 检测是否有数据
        return ('fail')
    data_get = request.data.decode('utf-8')

    data_json = json.loads(data_get)  # 把区获取到的数据转为JSON格式
    print(data_json['command'])
    # print(data_json['image'])

    return jsonify(data_json)  # 返回JSON数据。


if __name__ == '__main__':
    app.run(host='192.168.1.141', port=2021)
    # 这里指定了地址和端口号。
