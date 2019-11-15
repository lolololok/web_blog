from django.shortcuts import render
from django.views import View


class Index(View):
    """
    主页面
    """
    def get(self, request):
        try:
            """是否记住密码"""
            passwordinit = request.session.get("info").get("password")
            emailinit = request.session.get("info").get("email")
            check = request.session.get("info").get("check")
        except Exception as e:
            passwordinit = emailinit = ""
        return render(request, "index.html", locals())

