from flask_mail import Mail, Message

import random


def sendemail(email, app):
    """
    :param email: 用户邮箱
    :param app: 当前app
    :return: 验证码
    """
    app.config['MAIL_SERVER'] = 'smtp.163.com'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'm156011277053@163.com'
    app.config['MAIL_PASSWORD'] = 'LRc19980307'
    mail = Mail(app)
    captcha = ''

    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        captcha += ch
    message = Message('无问东西问答论坛邮箱验证码', sender=app.config['MAIL_USERNAME'],recipients=[email], body='您的验证码是：%s' % captcha)
    mail.send(message)
    return captcha

