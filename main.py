from flask import Flask, render_template
import json
app = Flask(__name__)


@app.route('/')
def index():
    """
    首页
    :return: index.html
    """
    pass
    return render_template("index.html")


@app.route('/helloworld')
def hello_world():
    """
    Hello World示例网页
    :return: helloworld.html
    """
    return render_template("helloworld.html")


@app.route('/jsonrequest')
def jsonrequest():
    """
    Jquery动态请求示例
    :return: Json格式请求结果
    """
    words = "Hello World!"
    wjson = json.dumps({"result": words})
    return wjson


if __name__ == "__main__":
    app.run(debug=True)

# def hello_world(example1, example2):
#     """
#     对函数或类的解释说明，要求所有函数、类、其中的关键部分注释要完整
#     :param example1: 对每个输入变量的解释说明
#     :param example2: 对每个输入变量的解释说明
#     :return: 对输出结果的解释说明
#     """
#     return example1 + example2

# 写完后应逐个检查右侧的warning，尽量要求不出现
