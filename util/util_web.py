from flask import request
from urllib.parse import urlparse, urljoin


def get_args(arg):
    """
    获取URL中的字段并检查安全性
    :param arg: str 字段名
    :return: str arg字段的内容
    """
    for target in request.args.get(arg), request.referrer:
        if not target:
            return None
        if is_safe_url(target):
            return target


def is_safe_url(target):
    """
    判断目标URL是否安全
    :param: str 目标URL
    :return: bool 是否安全
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
