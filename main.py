import json
from datetime import timedelta

from flask import Flask, redirect, render_template, request, session
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from werkzeug.contrib.cache import FileSystemCache

import login.Login as UtilLogin
from ask.collect import cancel_collect, collect
from ask.creatq import add
from ask.delet import delete
from ask.showdetail import to_answer, to_show_details
from ask.showq import query, queryA, queryCA, queryCQ
from ask.updat import updata
from classify.classify import Classifier
from login.Email import sendemail
from login.UserInformation import changeimage, get_avatar
from match.match import Matcher as UtilMatch
from recommend.recommend import recom_qid
from util.util_logging import UtilLogging
from util.util_mysql import Users, UtilMysql
from util.util_parameter import UtilParameter
from util.util_web import get_args

app = Flask(__name__)
app.secret_key = "7cWjrCrxe2MR68HTLwVUWQ=="
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

parameter = UtilParameter()
logger = UtilLogging(parameter, False, False, False)
mysql = UtilMysql(parameter.get_config("mysql"), logger)
cache = FileSystemCache('./.FILE/.cache')
classifier = Classifier()
labeldict = {"xuexi": "学习交流", "huodong": "活动通知",
             "xunwu": "寻物招领", "chushou": "二手出售", "qiugou": "二手求购",
             "huzhu": "互助问答", "zhaopin": "招聘求职"}


@app.route('/')
def index():
    """
    首页
    :return: index.html
    """
    return render_template("index.html")


@app.route('/helloworld')
@login_required
def hello_world():
    """
    Hello World示例网页
    :return: helloworld.html
    """
    return render_template("helloworld.html")

# Content Control -- start --
@app.route('/details/<qid>')
def details(qid):
    try:
        question, answers = to_show_details(qid, mysql)
        question.uname = mysql.select(Users, Users.uid == question.uid)[0].name
        for answer in answers:
            answer.uname = mysql.select(Users, Users.uid == answer.uid)[0].name
            answer.uavatar = get_avatar(answer.uid)
    except Exception as e:
        print(e)
        return render_template("error.html")
    return render_template('details.html', question=question, answers=answers)


@app.route('/search')
def search():
    """
    搜索页面，返回匹配问题
    """
    qtext = get_args("q")
    if not qtext:
        return render_template("search.html", labeldict=labeldict, q="", questions=[])
    matcher = UtilMatch(parameter.get_config("match"))
    qids = matcher.find(qtext, mysql, classifier)
    questions = mysql.get_ques(qids)
    try:
        for question in questions:
            question.uname = mysql.select(
                Users, Users.uid == question.uid)[0].name
            question.uavatar = get_avatar(question.uid)
    except Exception as e:
        print(e)
        return render_template("error.html")
    return render_template("search.html", labeldict=labeldict, q=qtext, questions=questions)


@app.route('/recommend')
def recommend():
    """
    推荐页面，区分登录、未登录，返回推荐问题
    """
    if current_user.is_anonymous:
        qids = recom_qid(args=parameter.get_config("recommend"), mysql=mysql)
    else:
        qids = recom_qid(args=parameter.get_config(
            "recommend"), mysql=mysql, user=current_user)
    questions = mysql.get_ques(qids)
    try:
        for question in questions:
            question.uname = mysql.select(
                Users, Users.uid == question.uid)[0].name
            question.uavatar = get_avatar(question.uid)
    except Exception as e:
        print(e)
        return render_template("error.html")
    return render_template("recommend.html", labeldict=labeldict, questions=questions)


@app.route('/classes/<label>')
def classes(label):
    """
    分类页面，按照分类返回问题
    """
    try:
        questions = query(uuid=None, uqid=None, ulabel=label, db=mysql)
        for question in questions:
            question.uname = mysql.select(
                Users, Users.uid == question.uid)[0].name
            question.uavatar = get_avatar(question.uid)
    except Exception as e:
        print(e)
        return render_template("error.html")
    return render_template("classes.html", label=labeldict.get(label), questions=questions)
# Content Control -- end --

# User Control -- start --
@app.route('/user')
@login_required
def user():
    """
    当前用户个人信息页
    """
    try:
        collectq = queryCQ(current_user.uid, mysql)
        collecta = queryCA(current_user.uid, mysql)
        questions = query(uuid=current_user.uid,
                          uqid=None, ulabel=None, db=mysql)
        answers = queryA(current_user.uid, mysql)
    except Exception as e:
        print(e)
        return render_template("error,html")
    return render_template("user.html",
                           avatar=get_avatar(current_user.uid), collecta=collecta, collectq=collectq,
                           questions=questions, answers=answers)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录功能、当前用户session注册和重定向逻辑
    """
    if request.method == 'GET':
        nexturl = get_args('next')
        if nexturl:
            session['next'] = nexturl
        else:
            session['next'] = request.referrer
        return render_template("login.html")
    else:
        user = UtilLogin.checkuser(request.form.get(
            'name'), request.form.get('passwd'), mysql)
        if isinstance(user, Users):
            if(request.form.get('remember') == 'on'):
                delta = timedelta(weeks=1)
                login_user(user, remember=True, duration=delta)
            else:
                login_user(user)
            nexturl = session.get('next')
            if nexturl:
                session.pop('next')
                if "/register" in nexturl:
                    nexturl = "/"
            else:
                nexturl = "/"
            return redirect(nexturl)
        else:
            return render_template("login.html", state=user)


@app.route('/register')
def register():
    """
    注册页面（不包含注册逻辑）
    """
    return render_template("register.html")


@app.route('/logout')
@login_required
def logout():
    """
    用户登出，清除用户session
    """
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    """
    Flask_login 用户构造器
    :param user_id: 用户ID
    :return: 用户对象
    """
    user = mysql.select(Users, Users.uid == user_id)
    if user:
        return mysql.select(Users, Users.uid == user_id)[0]
    else:
        return None
# User Control -- end --

# APIs -- start --
# API在login检查失败后返回login.html
@app.route('/api/register', methods=['POST'])
def register_api():
    """
    注册API接口
    :param: Request
    :return: json result: 0：用户名已被注册 1：密码不一致 2：邮箱格式有误
    3：邮箱已被注册 4：验证码已超时 5：验证码错误 -1：数据库错误 用户id：注册成功
    """
    state = UtilLogin.checkregister(request.form.get("name"), request.form.get(
        "password"), request.form.get("repeat"), request.form.get("email"), request.form.get("captcha"), mysql, cache)
    if state not in range(6):
        user = mysql.select(Users, Users.uid == state)
        if user:
            login_user(user[0])
        else:
            state = -1
    return json.dumps({"result": state})


@app.route('/api/sendmail', methods=['POST'])
def sendmail_api():
    """
    发送验证码API接口
    :param: Request
    :function: 管理验证码缓存，有效期可在配置文件中调整
    """
    emailadd = request.form.get("email")
    captchacache = cache.get(emailadd)
    if captchacache is None:
        captcha = sendemail(request.form.get("email"), app)
        cache.set(emailadd, captcha, 60 *
                  parameter.get_config("mail")["life_time"])
    else:
        sendemail(request.form.get("email"), app, captchacache)
    return "OK"


@app.route('/api/ask', methods=['POST'])
@login_required
def ask_api():
    """
    提问API接口
    :param: Request
    :return: OK：提问新增成功 Error：失败
    """
    title = request.form.get("title")
    content = request.form.get("content")
    anonymous = request.form.get("anonymous")
    label = classifier.get_label(title)
    try:
        add(current_user.uid, label, title, content, anonymous, mysql)
    except Exception as e:
        print(e)
        return "Error"
    return "OK"


@app.route('/api/answer', methods=['POST'])
@login_required
def answer_api():
    """
    回答API接口
    :param: Request
    :return: OK：回答新增成功 Error：失败
    """
    qid = request.form.get("qid")
    content = request.form.get("content")
    anonymous = request.form.get("anonymous")
    try:
        to_answer(current_user.uid, qid, content, anonymous, mysql)
    except Exception as e:
        print(e)
        return "Error"
    return "OK"


@app.route('/api/delete', methods=['POST'])
@login_required
def delete_api():
    """
    删除API接口
    :param: Request
    :return: AnsDel：回答删除成功 QuesDel：问题删除成功 Error：失败
    """
    qaid = request.form.get("id")
    try:
        state = delete(qaid, current_user.uid, mysql)
    except Exception as e:
        print(e)
        return "Error"
    return state


@app.route('/api/collect', methods=['POST'])
@login_required
def collect_api():
    """
    收藏API接口
    :param: Request id：问答ID query：是否仅查询
    :return: OK：成功 Duplicate：已收藏，重复操作 Not：未收藏 Error：失败
    """
    qaid = request.form.get("id")
    query = request.form.get("query")
    try:
        state = collect(qaid, current_user.uid, query, mysql)
    except Exception as e:
        print(e)
        return "Error"
    return state


@app.route('/api/cancel_collect', methods=['POST'])
@login_required
def cancel_collect_api():
    """
    取消收藏API接口
    :param: Request id：问答ID
    :return: OK：成功 Not：未收藏 Error：失败
    """
    qaid = request.form.get("id")
    try:
        state = cancel_collect(qaid, current_user.uid, mysql)
    except Exception as e:
        print(e)
        return "Error"
    return state


@app.route('/api/update_answer', methods=['POST'])
@login_required
def update_answer_api():
    """
    回答更新API接口
    :param: Request
    :return: OK：回答更新成功 NoAuth：无权限 Error：失败
    """
    aid = request.form.get("aid")
    content = request.form.get("content")
    anonymous = request.form.get("anonymous")
    try:
        state = updata(current_user.uid, aid, content, anonymous, mysql)
    except Exception as e:
        print(e)
        return "Error"
    return state


@app.route('/api/avatar', methods=['POST'])
def avatar_api():
    """
    头像更新API接口
    :param: Request
    :return: -1：图片不存在 0：图片格式不支持 1：更改完成
    """
    state = changeimage(current_user.uid, request.files["avatar-file"])
    return state
# APIs -- end --


if __name__ == "__main__":
    app.run(debug=True)
