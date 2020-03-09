from flask import Flask, render_template, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
import json
from ask import creatask, showask, updatask, delet, showdetail, collect
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
    uid = '2016404040404'
    qtitle = request.args.get("qtitle")
    qcontent = request.args.get("qcontent")
    qlabel = request.args.get("qlabel")
    print(qcontent, qlabel)
    creatask.add(uid, qlabel, qtitle, qcontent)
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


@app.route('/todeletq/<uqid>')
def todeletq(uqid):
    """
    删除问题
    :return: nothing
    """
    delet.delet_ques(None, uqid)
    return render_template("deleted.html")


@app.route('/todeleta/<uaid>')
def todeleta(uaid):
    """
    删除问题
    :return: nothing
    """
    delet.delet_ans(None, None, uaid)
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


# 展示问题详情界面
@app.route('/details/<qid>')
def details(qid):
    """
    展示问题详情
    :param qid: 问题ID
    :return:
    """
    question, answer = showdetail.to_show_details(qid)
    return render_template('showdetail.html', ques = question, ans = answer)


@app.route('/answered')
def is_answered():
    """
    回答函数
    :return:answered.html
    """
    # 未加入登录机制，默认使用一个uid
    uuid = "2016303030303"
    uqid = request.args.get("qid")
    acontent = request.args.get("acontent")
    print(uqid, acontent)
    showdetail.to_answer(uuid, uqid, acontent)
    return render_template("answered.html")


@app.route('/tocollectq/<qid>')
def tocollectq(qid):
    uid = "2016303030303"
    collect.to_collect_ques(uid, qid)
    return render_template("collected.html")


@app.route('/tocollecta/<aid>')
def tocollecta(aid):
    uid = "2016303030303"
    collect.to_collect_ans(uid, aid)
    return render_template("collected.html")


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
