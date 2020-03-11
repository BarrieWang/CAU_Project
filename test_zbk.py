# coding=utf-8
from flask import Flask, render_template, request, redirect, session, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from util.util_mysql import Users, UtilMysql, and_, Questions, Answers
from util.util_parameter import UtilParameter
from util.util_logging import UtilLogging
from util.util_web import get_args
from util.util_filter import UtilFilter
import uuid
from ask import creatq, showq, updat, delet, showdetail, collect
# 数据库连接，config.py为配置文件
# ===============================================================

app = Flask(__name__)
app.secret_key = "7cWjrCrxe2MR68HTLwVUWQ=="
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "yy_login"

parameter = UtilParameter()
logger = UtilLogging(parameter, False, False, False)
mysql = UtilMysql(parameter.get_config("mysql"), logger)
myfilter = UtilFilter(parameter.get_config("filter"))


@app.route('/')
def index():
    """
    首页
    :return: index.html
    """
    return render_template("index.html")


# ===============================================================
# 主页代码 --- 用于展示所有的问题 以及相应的答案链接
@app.route('/all')
def yy_main_page():
    questions = mysql.select(Questions)
    try:
        for question in questions:
            question.uname = mysql.select(Users, Users.uid == question.uid)[0].name
    except Exception:
        return render_template("error.html")
    context = {
        'questions': questions,
        # 'count':Count.query.all()
    }
    return render_template('yy_main.html', **context)

# 登陆界面 --- 用于让用户登陆 --- 若密码错误将会提示账号或密码错误
@app.route('/login', methods=['GET', 'POST'])
def yy_login():
    if request.method == 'GET':
        nexturl = get_args('next')
        if nexturl:
            session['next'] = nexturl
        else:
            session['next'] = request.referrer
        return render_template("yy_login.html")
    else:
        user = mysql.select(Users, and_(Users.name == request.form.get(
            'name'), Users.passwd == request.form.get('passwd')))
        if user:
            try:
                login_user(user[0])
            except Exception:
                return render_template("error.html")
            nexturl = session.get('next')
            if nexturl:
                session.pop('next')
            else:
                nexturl = "/"
            return redirect(nexturl)
        else:
            return render_template("yy_login.html")


# 注册页面 --- 用于新用户注册
@app.route('/regist/', methods=['GET', 'POST'])
def yy_regist():
    if request.method == 'GET':
        return render_template('yy_regist.html')
    if request.method == 'POST':
        name = request.form.get('name')
        passwd1 = request.form.get('passwd1')
        passwd2 = request.form.get('passwd2')
        user = mysql.select(Users, Users.name == name)
        if user:
            return u'已经被注册'
        if passwd1 != passwd2:
            return u'两次密码不相等'
        else:
            user = Users(uid="U"+str(uuid.uuid4().hex), name=name, passwd=passwd1)
            login_user(user)
            mysql.insert(user)
            return redirect("/")


# 主页展示
@app.route('/show/', methods=["GET", "POST"])
@login_required
def yy_show():
    if request.method == 'GET':
        return render_template('yy_show.html')
    else:
        ques_title = request.form.get('ques_title')
        ques_content = request.form.get('ques_content')
        ques_title, _ = myfilter.judge(ques_title)
        ques_content, _ = myfilter.judge(ques_content)
        uid = current_user.uid
        question = Questions(qid="Q"+str(uuid.uuid4().hex), ques_title=ques_title, ques_content=ques_content,)
        question.uid = uid
        mysql.insert(question)
        return redirect(url_for('yy_main_page'))


# 注销功能实现 --- 注销后跳转主页
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/creatask')
def to_creat_ask():
    """
    创建提问网页
    :return: creatq.html
    """
    return render_template("creatq.html")


@app.route('/created')
def is_created():
    """
    提示创建成功
    :return: created.html
    """
    # 用户ID暂时无法获取，默认一个
    uid = current_user.uid
    qtitle = request.args.get("qtitle")
    qcontent = request.args.get("qcontent")
    qlabel = request.args.get("qlabel")
    print(qcontent, qlabel)
    creatq.add(uid, qlabel, qtitle, qcontent)
    return render_template("created.html")


@app.route('/toupdatq/<uqid>')
def toupdatq(uqid):
    """
    修改问题
    :param uqid:问题ID
    :return updatq.html
    """
    uid = current_user.uid
    result, state = updat.query_qcontent(uid, uqid)
    if state == True:
        return render_template("updatq.html", res=result)
    else:
        return render_template("updated.html", state=state)


@app.route('/updatedq')
def is_updatedq():
    """
    提示修改操作结果
    :return: updated.html
    """
    uid = current_user.uid
    uqid = request.args.get("qid")
    uqtitle = request.args.get("qtitle")
    uqcontent = request.args.get("qcontent")
    uqlabel = request.args.get("qlabel")
    print(uqid, uqcontent, uqlabel)
    state = updat.updatq(uid, uqid, uqlabel, uqtitle, uqcontent)
    return render_template("updated.html", state=state)


@app.route('/toupdata/<uaid>')
def toupdata(uaid):
    """
    修改回答
    :return: updata.html
    """
    uid = current_user.uid
    qresult, aresult, state = updat.query_acontent(uid, uaid)
    print(qresult)
    print(aresult)
    if state == True:
        return render_template("updata.html", qres=qresult, ares=aresult)
    else:
        return render_template("updated.html", state=state)


@app.route('/updateda')
def is_updateda():
    """
    提示修改操作结果
    :return: updated.html
    """
    uid = current_user.uid
    uaid = request.args.get("aid")
    uacontent = request.args.get("acontent")
    state = updat.updata(uid, uaid, uacontent)
    return render_template("updated.html", state=state)

@app.route('/todeletq/<uqid>')
def todeletq(uqid):
    """
    删除问题
    :return: deleted.html
    :return: state:操作状态
    """
    uid = current_user.uid
    state = delet.delet_ques(uqid, uid)
    return render_template("deleted.html", state = state)


@app.route('/todeleta/<uaid>')
def todeleta(uaid):
    """
    删除回答
    :return: deleted.html
    :return: state:操作状态
    """
    uid = current_user.uid
    state = delet.delet_ans(uaid, uid)
    return render_template("deleted.html", state = state)


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
    result = showq.query(None, None, ulabel)
    print(result)
    return render_template("showask.html", result=result)


@app.route('/showask')
def showallask():
    """
    展示全部问题
    :return: showask.html
    """
    result = showq.query(None, None, None)
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
    uuid = current_user.uid
    uqid = request.args.get("qid")
    acontent = request.args.get("acontent")
    print(uqid, acontent)
    showdetail.to_answer(uuid, uqid, acontent)
    return render_template("answered.html")


@app.route('/tocollectq/<qid>')
def tocollectq(qid):
    uid = current_user.uid
    collect.to_collect_ques(uid, qid)
    return render_template("collected.html")


@app.route('/tocollecta/<aid>')
def tocollecta(aid):
    uid = current_user.uid
    collect.to_collect_ans(uid, aid)
    return render_template("collected.html")


@app.route('/toshowcollectq/<uid>')
def toshowcollectq(uid):
    """
    展示收藏问题
    :param uid:用户ID
    :return:收藏问题对象列表
    """
    res = showq.queryCQ(uid)
    return (render_template("showcollectq.html", result=res))


@app.route('/toshowcollecta/<uid>')
def toshowcollecta(uid):
    """
    展示收藏回答
    :param uid:用户ID
    :return:收藏回答对象列表
    """
    res = showq.queryCA(uid)
    return (render_template("showcollecta.html", result=res))


@app.route('/tocancelcollectq/<qid>')
def tocancelcollectq(qid):
    """
    取消收藏问题
    :param qid: 问题ID
    :return:
    """
    uid = current_user.uid
    collect.to_cancel_collectq(qid,uid)
    return redirect('/toshowcollectq/<uid>')


@app.route('/tocancelcollecta/<aid>')
def tocancelcollecta(aid):
    """
    取消收藏回答
    :param aid: 回答ID
    :return:
    """
    uid = current_user.uid
    collect.to_cancel_collecta(aid,uid)
    return redirect('/toshowcollecta/<uid>')


@login_manager.user_loader
def load_user(user_id):
    user = mysql.select(Users, Users.uid == user_id)
    if user:
        return mysql.select(Users, Users.uid == user_id)[0]
    else:
        return None


if __name__ == '__main__':
    app.run(debug=True)
