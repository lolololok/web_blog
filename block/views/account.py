from django.shortcuts import render, redirect, HttpResponse
from django.http.response import JsonResponse
from block.forms import RegisterForms
from email.mime.text import MIMEText
from django.contrib import auth
from django.db.models import Q
from geetest import GeetestLib
from django.views import View
from .blog import settings
from block import models
import smtplib
import random
import uuid
import time
import os


class Register(View):
    """
    用户注册
    """
    def get(self, request):
        """
        获取用户注册页面
        :param request:
        :return:
        """
        form_obj = RegisterForms()
        return render(request, "register.html", locals())

    def post(self, request):
        """
        用户注册信息校验，有钩子校验
        :param request:
        :return:
        """
        if request.method == "POST":
            ret = {'status': 0, 'msg': ''}
            form_obj = RegisterForms(request.POST)
            # 帮我做校验
            if form_obj.is_valid():
                # 校验通过去数据库健一个新的数据
                form_obj.cleaned_data.pop("repassword")
                img_ava = request.FILES.get('img-ava')
                if img_ava:
                    if img_ava.size > 524288000:
                        ret['status'] = 1
                        ret['msg'] = "图片文件大于5M"
                        return JsonResponse(ret)
                    uid = str(uuid.uuid1())  # uid作为图片后缀
                    path = os.path.join(settings.MEDIA_ROOT, 'head_img', uid + ".jpg")
                    with open(path, 'wb') as f:  # 保存图片
                        for line in img_ava:
                            f.write(line)
                    models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar="head_img/" + uid + ".jpg")
                else:
                    models.UserInfo.objects.create_user(**form_obj.cleaned_data)  # 未选择图片，使用默认图片
                ret['msg'] = '/api/v1/index/'  # 注册成功返回路径
                return JsonResponse(ret)
            else:
                ret['status'] = 1
                ret['msg'] = form_obj.errors  # form表单格式不正确
                return JsonResponse(ret)


class CheckUserExist(View):
    """
    检测用户是否存在
    """
    def get(self, request):
        """
        检测email
        :param request:
        :return:
        """
        ret = {'status': 0, 'msg': ''}
        email = request.GET.get('email')
        is_exist = models.UserInfo.objects.filter(email=email).first()
        if is_exist:
            ret['status'] = 1
            ret['msg'] = '用户已存在'
        else:
            ret['status'] = 0
            ret['msg'] = ''
        return JsonResponse(ret)


pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"# 请在官网申请ID使用，示例ID不可使用
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


class GetGeetest(View):
    """
    极验校验
    """
    def get(self, request):
        user_id = 'test'
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        status = gt.pre_process(user_id)
        request.session[gt.GT_STATUS_SESSION_KEY] = status
        request.session["user_id"] = user_id
        response_str = gt.get_response_str()
        return HttpResponse(response_str)


class Login(View):
    """
    登录
    """
    def get(self, request):
        """
        获取登录页面：模态框
        :param request:
        :return:
        """
        ret = {"code": 1000, "msg": ""}
        login_info = request.GET.get("email")
        if not models.UserInfo.objects.filter(Q(email=login_info) | Q(username=login_info)).first():
            ret["code"] = 1001
            ret["msg"] = "用户不存在"
        return JsonResponse(ret)

    def post(self, request):
        """
        登录提交校验
        :param request:
        :return:
        """
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        login_info = request.POST.get('email')
        password = request.POST.get('password')
        check = request.POST.get("check")
        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]  # 极验校验
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码正确
            user_obj = models.UserInfo.objects.filter(Q(email=login_info) | Q(username=login_info)).first()
            if user_obj:
                user = user_obj.check_password(password)  # y用户存在，且密码正确
            else:
                user = False
            if user:
                # 用户名密码正确
                # 给用户做登录(将登陆用户赋值给request.user)
                if check == "true":   # 记住密码
                    info = {
                        "check": "checked",
                        "email": login_info,
                        "password": password
                    }
                    request.session["info"] = info
                request.session["uid"] = user_obj.nid
                ret["msg"] = "/api/v1/bowen/"  # 用户返回界面
                auth.login(request, user_obj)  # 注册用户到request
            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["msg"] = "验证码错误"
            ret["status"] = 1
        return JsonResponse(ret)


class LoginOut(View):
    """
    注销
    """
    def get(self, request):
        request.session.flush()
        return redirect("/api/v1/index/")


class RePassword(View):
    """
    修改密码
    """
    def get(self, request):
        """
        返回修改密码页面
        :param request:
        :return:
        """
        return render(request, "re-password.html")

    def post(self, request):
        """
        提交修改信息
        :param request:
        :return:
        """
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        ret = {"code": 1000, "msg": ""}
        user_obj = models.UserInfo.objects.get(nid=request.user.nid)
        if user_obj.check_password(password):
            user_obj.set_password(repassword)
            user_obj.save()
            return redirect("/api/v1/index/")  # 修改成功返回界面
        else:
            ret["code"] = 1001
            ret["msg"] = "原始密码不正确"
        return render(request, "re-password.html", {"ret": ret})


class ReInfo(View):
    """
    修改用户信息：用户名，签名，头像
    """
    def get(self, request):
        """
        获取原始信息
        :param request:
        :return:
        """
        form_obj = RegisterForms(
            initial={
                "username": request.user.username,
                "sign": request.user.sign,
            }
        )
        return render(request, "re-info.html", locals())

    def post(self, request):
        """
        获取提交信息
        :param request:
        :return:
        """
        erro = ""
        username = request.POST.get("username")
        sign = request.POST.get("sign")
        avatar = request.FILES.get("avatar")
        if models.UserInfo.objects.exclude(nid=request.user.nid).filter(username=username):  # 和别人名字一样了
            erro = "用户名已存在"
            form_obj = RegisterForms(
                initial={
                    "username": username,
                    "sign": request.user.sign,
                }
            )
            return render(request, "re-info.html", locals())
        if avatar and avatar.size > 524288000:
            erro = "图片文件大于5M"
            form_obj = RegisterForms(
                initial={
                    "username": username,
                    "sign": request.user.sign,
                }
            )
            return render(request, "re-info.html", locals())
        if not avatar:
            models.UserInfo.objects.filter(nid=request.user.nid).update(
                username=username,
                sign=sign
            )
        elif request.user.avatar:
            os.remove(request.user.avatar.path)
            uid = str(uuid.uuid1())
            models.UserInfo.objects.filter(nid=request.user.nid).update(
                username=username,
                sign=sign,
                avatar="head_img/" + uid + ".jpg"
            )
            path = os.path.join(settings.MEDIA_ROOT, 'head_img', uid + ".jpg")
            with open(path, 'wb') as f:
                for line in avatar:
                    f.write(line)
        return redirect("/api/v1/bowen/")


class RetrievePassword(View):
    """
    找回密码
    """
    def get(self, request):
        return render(request, "retrieve-password.html")

    def post(self, request):
        ret = {"code": 1000, "msg": ""}
        code = request.POST.get("code")
        email = request.POST.get("email")
        pwd = request.POST.get("pwd")
        repwd = request.POST.get("repwd")
        if not code:
            ret["code"] = 1001
            ret["msg"] = "验证码输入有误"
            return JsonResponse(ret)
        pwd_isval = pwd == repwd
        if not pwd_isval:
            ret["code"] = 1002
            ret["msg"] = "两次密码不一致"
            return JsonResponse(ret)
        try:
            now_time = time.time()
            if request.session.get("email_code", ""):
                time_erro = now_time - request.session.get("email_code").get("start_time")
                if time_erro > 60:
                    ret["code"] = 1003
                    ret["msg"] = "验证码过时"
                else:
                    code_isval = code == request.session.get("email_code").get("code")
                    if code_isval:
                        email_obj = models.UserInfo.objects.get(email=email)
                        email_obj.set_password(repwd)
                        email_obj.save()
                        # del request.session["email_code"]
                    else:
                        ret["code"] = 1004
                        ret["msg"] = "验证码输入不正确"
            else:
                ret["code"] = 1005
                ret["msg"] = "请获取验证码"
        except Exception:
            ret["code"] = 1006
            ret["msg"] = "找回密码失败"
        return JsonResponse(ret)


class EmailYanzheng(View):
    """
    邮箱验证
    """
    msg_from = '1576340464@qq.com'  # 发送方邮箱
    passwd = 'acpxdlrhregyiibi'  # 填入发送方邮箱的授权码
    subject = "小小龙博客密码找回 ^_^"  # 主题
    content = "你的验证码是{}请您收好，密码修改成功后请管理好您的密码"  # 正文

    def code(self, n=6):
        s = ''  # 创建字符串变量,存储生成的验证码
        for i in range(n):  # 通过for循环控制验证码位数
            num = random.randint(0, 9)  # 生成随机数字0-9
            s = s + str(num)
        return s

    def send_msg(self, content="", subject="", isfrom="", isto="", shpwd=""):
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = isfrom
        msg['To'] = isto
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
            s.login(isfrom, shpwd)
            s.sendmail(isfrom, isto, msg.as_string())
            s.quit()
            return True
        except Exception:
            return False

    def get(self, request):
        ret = {"status": 1000, "msg": ""}
        email = request.GET.get("email")
        code = self.code()
        request.session["email_code"] = {"code": code, "start_time": time.time()}
        contents = self.content.format(code)
        isvail = self.send_msg(
            content=contents,
            subject=self.subject,
            isfrom=self.msg_from,
            isto=email,
            shpwd=self.passwd
        )
        if not isvail:
            ret["status"] = 1001
            ret["msg"] = "验证码获取失败"
        return JsonResponse(ret)


class EmailCheck(View):
    """
    邮箱是否注册验证
    """
    def get(self, request):
        ret = {"code": 1000, "msg": ""}
        email = request.GET.get("email")
        email_obj = models.UserInfo.objects.filter(email=email).first()
        if not email_obj:
            ret["code"] = 1001
            ret["msg"] = "邮箱未{}".format("<a href='/api/v1/register/'>注册</a>")
        return JsonResponse(ret)