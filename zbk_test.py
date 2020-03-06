from flask import Flask, render_template, request
import json
from ask import creatask, showask, updatask, deletask
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


@app.route('/creatask')
def to_creat_ask():
    """
    创建提问网页
    :return: creatask.html
    """
    return render_template("creatask.html")


@app.route('/created')
def is_created():
    """
    提示创建成功
    :return: created.html
    """
    # 用户ID暂时无法获取，默认一个
    uuid = '2016404040404'
    uqcontent = request.args.get("qcontent")
    uqlabel = request.args.get("qlabel")
    print(uqcontent, uqlabel)
    creatask.add(uuid, uqlabel, uqcontent)
    return render_template("created.html")


@app.route('/toupdatask/<uqid>')
def toupdatask(uqid):
    """
    x修改问题
    :return: updatask.html
    """
    result = updatask.query(uqid)
    return render_template("updatask.html", res=result)


@app.route('/updated')
def is_updated():
    """
    提示创建成功
    :return: updated.html
    """
    uqid = request.args.get("qid")
    uqcontent = request.args.get("qcontent")
    uqlabel = request.args.get("qlabel")
    print(uqid, uqcontent, uqlabel)
    updatask.updat(uqid, uqlabel, uqcontent)
    return render_template("updated.html")


@app.route('/todeletask/<uqid>')
def todelet(uqid):
    """
    删除问题
    :return: nothing
    """
    deletask.delet_ques(uqid)
    return render_template("deleted.html")


@app.route('/showlabel')
def to_show_label():
    """
    展示问题分类
    :return: showlabel.html
    """
    return render_template("showlabel.html")


@app.route('/toshowask/<ulabel>')
def toshowask(ulabel):
    """
    展示某类问题
    :return:showask.html
    """
    result = showask.query(None, None, ulabel)
    print(result)
    return render_template("showask.html", result=result)


@app.route('/showask')
def showallask():
    """
    展示全部问题
    :return: showask.html
    """
    result = showask.query(None, None, None)
    print(result)
    return render_template("showask.html", result=result)


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
