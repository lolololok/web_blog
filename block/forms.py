from django.forms import widgets, ValidationError
from django import forms
from block import models


class RegisterForms(forms.Form):
    username = forms.CharField(
        max_length=16,
        label='用户名',
        error_messages={
            'max_length': '用户名过长',
            'required': '用户名不能为空',
        },
        widget=widgets.TextInput(
            attrs={'class': 'form-control'},
        )
    )
    password = forms.CharField(
        min_length=5,
        label='密码',
        widget=widgets.PasswordInput(
            attrs={'class': 'form-control'},
            render_value=True
        ),
        error_messages={
            'min_length': '密码至少要5位',
            'required': '密码不能为空'
        }

    )
    repassword = forms.CharField(
        min_length = 5,
        label='确认密码',
        widget=widgets.PasswordInput(
            attrs={'class': 'form-control'}
        ),
        error_messages={
            'min_length': '密码至少要5位',
            'required': '密码不能为空',
        }

    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control'}
        ),
        error_messages={
            'invalid': '邮箱格式不正确',
            'required': '邮箱不能为空',
        }
    )
    sign = forms.CharField(
        label='个性签名',
        widget=forms.widgets.Textarea(
            attrs={'class': 'form-control'}
        ),
        error_messages={
            'required': '个性签名不能为空',
        }
    )

    # 重写全局的钩子函数，对确认密码做校验
    def clean(self):
        password = self.cleaned_data.get('password')
        repassword = self.cleaned_data.get('repassword')
        if repassword and repassword != password:
            self.add_error('repassword', ValidationError('两次密码不一致'))
        else:
            return self.cleaned_data

    # 重写username字段局部钩子检测用户是否已存在
    def clean_username(self):
        username = self.cleaned_data.get('username')
        is_exist = models.UserInfo.objects.filter(username=username)
        if is_exist:
            # 表示用户已存在
            self.add_error('username', ValidationError('用户已存在'))
        else:
            return username

    # 重写email字段局部钩子检测email是否已存在
    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exist = models.UserInfo.objects.filter(email=email)
        if is_exist:
            # 表示email已存在
            self.add_error('email', ValidationError('email已存在'))
        else:
            return email

    # 重写email字段局部钩子检测sign是否太长
    def clean_sign(self):
        sign = self.cleaned_data.get('sign')
        if len(sign) > 20:
            self.add_error('sign', ValidationError('字数不能超过20字'))
        else:
            return sign


class ArticleAddForms(forms.Form):
    """
    文章添加form表单
    """
    title = forms.CharField(
        max_length=100,
        label='文章标题',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'},
        )
    )
    tags = forms.CharField(
        max_length=100,
        label='标签',
        widget=widgets.TextInput(
            attrs={'class': 'form-control'},
        ),
        error_messages={
            'required': '标签不能为空',
        }
    )
    category_list = (
        (1, "人工智能"),
        (2, "移动开发"),
        (3, "物联网"),
        (4, "架构"),
        (5, "云计算/大数据"),
        (6, "互联网"),
        (7, "游戏开发"),
        (8, "运维"),
        (9, "数据库"),
        (10, "前端"),
        (11, "后端"),
        (12, "编程语言"),
        (13, "研发管理"),
        (14, "安全"),
        (15, "程序人生"),
        (16, "区块链"),
        (17, "音视频开发"),
        (18, "资讯"),
        (19, "计算机理论与基础"),
        (20, "闲杂论坛"),
    )
    category = forms.CharField(
        label='分类',
        widget=widgets.Select(
            attrs={'class': 'form-control'},
            choices=category_list
        )
    )

    # 重写title字段局部钩子检测title是否太长
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 25:
            self.add_error('title', ValidationError('文章标题不能超过25字'))
        else:
            return title

