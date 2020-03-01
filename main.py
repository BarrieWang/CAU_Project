from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world(example1, example2):
    """
    对函数或类的解释说明，要求所有函数、类、其中的关键部分注释要完整
    :param example1: 对每个输入变量的解释说明
    :param example2: 对每个输入变量的解释说明
    :return: 对输出结果的解释说明
    """
    return example1 + example2

# 写完后应逐个检查右侧的warning，尽量要求不出现
