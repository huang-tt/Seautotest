# coding=utf-8

import flask, json

server = flask.Flask(__name__)  # __name__代表当前的python文件。把当前的python文件当做一个服务启动


@server.route('/index', methods=['get', 'post'])  # 第一个参数就是路径,第二个参数支持的请求方式，不写的话默认是get
def index():
    res = {'msg': '这是我开发的第一个接口', 'msg_code': 1}
    return json.dumps(res, ensure_ascii=False)

server.run(port=8888, debug=True, host='127.0.0.1')