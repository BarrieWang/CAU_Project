from flask import Flask, render_template, request, flash, session
from login.Login import *
from util.util_mysql import *
from util.util_logging import *
from util.util_parameter import *
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'


@app.route('/')
def index():
    """
    首页
    :return: index.html
    """
    parameter = UtilParameter()
    logger = UtilLogging(parameter, False, False, False)
    global db
    db = UtilMysql(parameter.get_config("mysql"), logger)
    pass
    return render_template("register.html", result=4)


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


@app.route('/UserLogin', methods=['POST'])
def log_in():
    """
    UserLogin：用户注册
    :return: result=0：无用户名 result=1：密码不正确 用户数据库对象：登陆成功
    """
    if request.form['login'] == "登录":
        username = request.form.get('username')
        password = request.form.get('password')
        result = checkuser(username, password, db)
        if(result == 0 or result == 1):
            return render_template("login.html", result=result)
        else:
            session['userid'] = result.uid
            # print(session.get('userid'))
            return render_template("helloworld.html")
    elif request.form['login'] == "注册":
        return render_template("register.html", result=3)


@app.route('/UserRegister', methods=['POST'])
def register_user():
    """
    :return: 0：用户名已被注册 1：密码不一致 2：邮箱格式有误 3：邮箱已被注册 4：注册成功
    """
    username = request.form.get('username')
    password = request.form.get('password')
    repeatpasswd = request.form.get('repeat')
    useremail = request.form.get('email')
    result = checkregister(username, password, repeatpasswd, useremail, db)
    print(result)
    if(result == 0 or result == 1 or result == 2 or result == 3):
        return render_template("register.html", result=result)
    else:
        session['userid'] = result
        flash("注册成功！选择您的兴趣点")
        return render_template("chooseinterest.html", result=result)


@app.route('/UserInterest', methods=['POST'])
def choose_interest():
    """
    UserLogin：用户注册
    :return: result=0：无用户名 result=1：密码不正确 用户数据库对象：登陆成功
    """
    interest = str()
    for i in range(1, 6):
        if request.form.get(str(i)) is not None:
            interest += str(i) + ','
    if storeinterest(interest, session.get('userid'), db):
        return render_template("helloworld.html")


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
