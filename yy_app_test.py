# coding=utf-8

from flask import Flask,render_template,request,url_for,redirect,session
# from exists import db
import config
import os
from models import User,Question,Answers,Count
from decorators import login_limit
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# 数据库连接，config.py为配置文件
# ===============================================================
db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
# ===============================================================
# 主页代码 --- 用于展示所有的问题 以及相应的答案链接
@app.route('/')
def yy_main_page():
    context = {
        'questions': Question.query.all(),
        #'count':Count.query.all()
    }
    return render_template('yy_main.html', **context)

# 登陆界面 --- 用于让用户登陆 --- 若密码错误将会提示账号或密码错误
@app.route('/yy_login/',methods=['GET','POST'])
def yy_login():
    if request.method == 'GET':
        return render_template('yy_login.html')
    if request.method == 'POST':
        name = request.form.get('name')
        passwd = request.form.get('passwd')
        user = User.query.filter(User.name == name, User.passwd == passwd).first()
        if user:
            session['user_id'] = user.uid
            session.permanent = True
            return redirect(url_for('yy_main_page'))
        # not the function render_template()
        else:
            return u'账号或密码错误'

# 注册页面 --- 用于新用户注册
@app.route('/yy_regist/',methods=['GET','POST'])
def yy_regist():
    if request.method == 'GET':
        return render_template('yy_regist.html')
    if request.method == 'POST':
        name = request.form.get('name')
        passwd1 = request.form.get('passwd1')
        passwd2 = request.form.get('passwd2')
        user = User.query.filter(User.name == name).first()
        if user:
            return u'已经被注册'
        if passwd1 != passwd2:
            return u'两次密码不相等'
        else:
            user = User(name=name,passwd=passwd1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('yy_login'))

# 主页展示
@app.route('/yy_show/', methods=["GET","POST"])
@login_limit
def yy_show():
    if request.method == 'GET':
        return render_template('yy_show.html')
    else:
        ques_title = request.form.get('ques_title')
        ques_content = request.form.get('ques_content')
        uid = session.get('uid')
        user = User.query.filter(User.uid == uid).first()
        question = Question(ques_title=ques_title,ques_content=ques_content,)
        question.uid = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('yy_main_page'))

# 注销功能实现 --- 注销后跳转主页
@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('yy_login'))

# 限制登陆功能实现
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.uid == user_id).first()
        return {'user': user}
    return {}

# 展示话题详情界面
@app.route('/yy_details/<qid>')
def yy_details(qid):
    question = Question.query.filter(Question.qid == qid).first()
    return render_template('yy_details.html', question = question)

# 发表回答的界面
@app.route('/add_answer/', methods=['POST'])
@login_limit
def add_answer():
    ans_content = request.form.get('ans_content')
    qid = request.form.get('qid')
    answer = Answers(ans_content=ans_content)
    uid = session.get('user_id')
    user = User.query.filter(User.uid == uid).first()
    question = Question.query.filter(Question.qid == qid).first()
    answer.author = user
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('yy_details',qid=qid))
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
