from flask_mail import Mail, Message
from threading import Thread
import random


def sendemail(email, app, captcha=None):
    """
    :param email: 用户邮箱
    :param app: 当前app
    :param captcha: 验证码，为空时生成新验证码，否则发送传入值
    :return: 验证码
    """
    app.config['MAIL_SERVER'] = 'smtp.163.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'm156011277053@163.com'
    app.config['MAIL_PASSWORD'] = 'LRc19980307'
    mail = Mail(app)
    if captcha is None:
        captcha = ''
        for i in range(6):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            captcha += ch
    message = Message('无问东西 - 邮箱验证码', sender=("WuWenXiDong Group", app.config['MAIL_USERNAME']), recipients=[
                      email], body='感谢您的使用！\n\n您的验证码是：%s\n\n验证码10分钟内有效。' % captcha)
    thr = Thread(target=send_async_email, args=[app, mail, message])
    thr.start()
    return captcha


def send_async_email(app, mail, msg):
    with app.app_context():
        mail.send(msg)
