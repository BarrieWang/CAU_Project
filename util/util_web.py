from flask import request
from urllib.parse import urlparse, urljoin


def get_next():
    """
    获取URL中的next字段并检查安全性
    :return: str next字段url
    """
    for target in request.args.get('next'), request.referrer:
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
