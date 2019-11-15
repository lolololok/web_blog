"""myblock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from block.views import account, index, blog
from django.conf import settings             # 新加入
from django.conf.urls.static import static   # 新加入


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/index/$', index.Index.as_view(), name="index"),

    # # 极验滑动验证码 获取验证码的url
    url(r'^pc-geetest/register/$', account.GetGeetest.as_view()),
    url(r'^api/v1/register/$', account.Register.as_view(), name="register"),
    url(r'^api/v1/register_check/$', account.CheckUserExist.as_view(), name="check"),
    url(r'^api/v1/login/$', account.Login.as_view(), name="login"),
    url(r'^api/v1/loginout/$', account.LoginOut.as_view(), name="loginout"),
    url(r'^api/v1/repassword/$', account.RePassword.as_view(), name="repassword"),
    url(r'^api/v1/reinfo/$', account.ReInfo.as_view(), name="reinfo"),
    url(r'^api/v1/retrpwd/$', account.RetrievePassword.as_view(), name="retrpwd"),
    url(r'^api/v1/emailva/$', account.EmailYanzheng.as_view(), name="emailva"),
    url(r'^api/v1/emailcheck/$', account.EmailCheck.as_view(), name="emailcheck"),

    #
    url(r'^api/v1/blog/', blog.Blog.as_view(), name="blog"),

    url(r'^api/v1/bowen/$', blog.Bowen.as_view(), name="bowen"),

    url(r'^api/v1/article/top/$', blog.Top.as_view(), name="top"),

    url(r'^api/v1/article/show/$', blog.ShowContent.as_view(), name="show"),

    url(r'^api/v1/article/updown/$', blog.UpDown.as_view(), name="updown"),

    url(r'^api/v1/article/comment/$', blog.Comment.as_view(), name="comment"),

    url(r'^api/v1/upload/$', blog.Upload.as_view(), name="upload"),

    url(r'^api/v1/editarticle/$', blog.EditArticle.as_view(), name="editarticle"),

    url(r'^api/v1/deletearticle/$', blog.DeleteArticle.as_view(), name="deletearticle"),

    url(r'^api/v1/addarticle/$', blog.AddArticle.as_view(), name="addarticle"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
