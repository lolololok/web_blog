from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
import re


URL = [
    '/api/v1/register/',
    '/admin/.*',
    'api/v1/register_check/',
    '/api/v1/index/',
    '/api/v1/login/',
    '/pc-geetest/register/',
    '/api/v1/upload/',
    '/api/v1/index/',
    '/api/v1/retrpwd/',
    '/api/v1/emailva/',
    '/api/v1/emailcheck/'
]


class RequestAllow(MiddlewareMixin):
    """
    请求验证中间件
    """
    def process_request(self, request):
        current_path = request.path
        for valid_url in URL:
            ret = re.match(valid_url, current_path)
            if ret:
                return None
        else:
            if request.session.get("uid"):
                return
            else:
                return redirect("/api/v1/index/")