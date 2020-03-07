# coding=utf-8
from flask import Flask, render_template, request, redirect, session, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from util.util_mysql import Users, UtilMysql, and_, Questions, Answers
from util.util_parameter import UtilParameter
from util.util_logging import UtilLogging
from util.util_web import get_args
from util.util_filter import UtilFilter
import uuid
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
    for question in questions:
        question.uname = mysql.select(Users, Users.uid == question.uid)[0].name
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
            login_user(user[0])
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


# 展示话题详情界面
@app.route('/details/<qid>')
def yy_details(qid):
    question = mysql.select(Questions, Questions.qid == qid)[0]
    question.uname = mysql.select(Users, Users.uid == question.uid)[0].name
    answers = mysql.select(Answers, Answers.qid == question.qid)
    for answer in answers:
        answer.uname = mysql.select(Users, Users.uid == answer.uid)[0].name
    return render_template('yy_details.html', question=question, answers=answers)

# 发表回答的界面
@app.route('/add_answer', methods=['GET', 'POST'])
@login_required
def add_answer():
    if request.method == 'GET':
        sourceurl = get_args('source')
        return redirect('/details/'+sourceurl)
    ans_content = request.form.get('ans_content')
    ans_content, _ = myfilter.judge(ans_content)
    qid = request.form.get('qid')
    answer = Answers(aid="A"+str(uuid.uuid4().hex), ans_content=ans_content)
    uid = current_user.uid
    answer.uid = uid
    answer.qid = qid
    mysql.insert(answer)
    return redirect(url_for('yy_details', qid=qid))


@login_manager.user_loader
def load_user(user_id):
    user = mysql.select(Users, Users.uid == user_id)
    if user:
        return mysql.select(Users, Users.uid == user_id)[0]
    else:
        return None


'''
# 这个不太对
# 实现收藏功能
@app.route('/upgrade/<question_id>',methods=['GET'])
def upgrade(question_id):
    question = Question.query.filter(Question.id == question_id).first()
    question.like_count+=1
    db.session.commit()
    return redirect(url_for('yy_details',question_id=question_id))
'''
if __name__ == '__main__':
    app.run(debug=True)
