from django.shortcuts import render, redirect, HttpResponse
from django.http.response import JsonResponse
from block.forms import ArticleAddForms
from ..utils.page import Pagination
from django.db.models import F, Q
from django.conf import settings
from django.views import View
from bs4 import BeautifulSoup
from block import models
import uuid
import json
import os


class Blog(View):
    def get(self, request):
        """
        获取个人文章列表信息
        :param request:
        :return:
        """
        try:
            """如果有置顶文章就置顶"""
            article_id = models.Top.objects.filter(user=request.user).first().article
            article_top_obj = models.Article.objects.filter(nid=article_id).first()
        except Exception as e:
            pass
        blog_obj = models.Article.objects.filter(user=request.user).all().order_by("-create_time")  # 按照时间的从大到小
        if request.GET:
            if request.GET.get("tag") == "1":  # 所有指定标签的文章
                blog_obj = models.Article.objects.filter(tags__nid=request.GET.get("id"), user=request.user)
            elif request.GET.get("tag") == "2":  # 所有指定分类的文章
                blog_obj = models.Article.objects.filter(category_id=request.GET.get("id"), user=request.user)
            elif request.GET.get("tag") == "3":  # 所有指定日期的文章
                date_year_month = request.GET.get("id").split("-")
                blog_obj = models.Article.objects.filter(
                    Q(create_time__year=int(date_year_month[0])) | Q(create_time__month=int(date_year_month[1]))
                ).filter(user=request.user).all().order_by("-create_time")
        pagination = Pagination(
            request.GET.get("page", 1),
            len(blog_obj),
            request.path,
            request.GET,
            per_page_num=10,
            pager_count=5
        )   # 对文章进行分页
        blog_obj = blog_obj[pagination.start:pagination.end]
        return render(request, "blog.html", locals())


class Bowen(View):
    """
    所有文章
    """
    def get(self, request):
        article_obj = models.Article.objects.all().order_by("-create_time")  # 选出所有文章，日期从大到小
        if request.GET.get("uid"):  # 若点了某个人
            article_obj = models.Article.objects.filter(user_id=int(request.GET.get("uid"))).all()
        pagination = Pagination(
            request.GET.get("page", 1),
            len(article_obj),
            request.path,
            request.GET,
            per_page_num=10,
            pager_count=5
        )
        article_obj = article_obj[pagination.start:pagination.end]
        return render(request, "article-others.html", locals())

    def post(self, request):
        """
        文章搜索：写不是很好XXX
        :param request:
        :return:
        """
        searchinput = request.POST.get("searchinput")
        article_obj = models.Article.objects.filter(title__contains=searchinput).all()
        return render(request, "article-others.html", locals())


class AddArticle(View):
    """
    添加文章
    """
    def get(self, request):
        form_obj = ArticleAddForms()
        return render(request, "add-article.html", locals())

    def post(self, request):
        try:
            form_obj = ArticleAddForms(request.POST)
            if not form_obj.is_valid():
                return render(request, "edit-article.html", {"form_obj": form_obj})
            title = request.POST.get("title")
            category = request.POST.get("category")
            content = request.POST.get("article_content")
            bs = BeautifulSoup(content, "html.parser")
            desc = bs.text.strip()[0:50] + "..."
            for tag in bs.find_all():
                if tag.name in ['script', 'link']:
                    tag.decompose()  # 剔除非法标签
            category_obj = models.Category.objects.filter(
                title=ArticleAddForms.category_list[int(category) - 1][1]).first()
            if category_obj:
                category_obj = category_obj  #若已有这个分类，就绑定这个分类
            else:
                category_obj = models.Category.objects.create(
                    title=ArticleAddForms.category_list[int(category) - 1][1])
            article_obj = models.Article.objects.create(
                title=title,
                desc=desc,
                category=category_obj,
                user=request.user,
            )
            models.ArticleDetail.objects.create(article=article_obj, content=str(content))
            tag_list = request.POST.get("tags").strip().split(",")
            tag_list_obj = []
            if tag_list:
                for tag in tag_list:
                    tag_obj = models.Tag.objects.filter(title=tag).first()  # 若已有这个标签就使用已有的
                    if tag_obj:
                        tag_obj = tag_obj
                    else:
                        tag_obj = models.Tag.objects.create(title=tag)
                    tag_list_obj.append(tag_obj)
                for obj in tag_list_obj:
                    models.Article2Tag.objects.create(article=article_obj, tag=obj)
            return redirect("/api/v1/blog/")
        except Exception as e:
            return HttpResponse("呀！好像出错了>_<")  # 添加失败


class EditArticle(View):
    """
    文章编辑
    """
    def get(self, request):
        """
        获取文章原始信息
        :param request:
        :return:
        """
        article_id = int(request.GET.get("id"))
        request.session["article_id"] = article_id
        article_obj = models.Article.objects.filter(nid=article_id).first()
        title = article_obj.title
        content = article_obj.articledetail.content
        tags = article_obj.tags.all()
        if tags:
            tag_list = [tag.title for tag in tags]
            tag_list = ",".join(tag_list)
        else:
            tag_list = ""
        category = article_obj.category.title
        for t in ArticleAddForms.category_list:
            if t[1] == category:
                category = t[0]
                break  # 选出文章分类编号
        form_obj = ArticleAddForms(
            initial={"title": title, "tags": tag_list, "category": [category, ]})
        return render(request, "edit-article.html", locals())

    def post(self, request):
        """
        提交修改数据
        :param request:
        :return:
        """
        try:
            form_obj = ArticleAddForms(request.POST)
            if not form_obj.is_valid():
                return render(request, "edit-article.html", {"form_obj": form_obj})
            title = request.POST.get("title")
            category = request.POST.get("category")
            content = request.POST.get("article_content")
            bs = BeautifulSoup(content, "html.parser")
            desc = bs.text.strip()[0:50] + "..."
            for tag in bs.find_all():
                if tag.name in ['script', 'link']:
                    tag.decompose()
            article_obj = models.Article.objects.filter(nid=request.session.get("article_id")).first()
            articledetail_obj = article_obj.articledetail
            articledetail_obj.content = str(bs)
            articledetail_obj.save()
            tags = article_obj.tags.all()
            if tags:
                for item in tags:
                    models.Article2Tag.objects.filter(tag=item).delete()
                    item.delete()  # 删除原有标签
            category_obj = article_obj.category
            category_obj.title = ArticleAddForms.category_list[int(category) - 1][1]
            category_obj.save()
            article_obj.title = title
            article_obj.desc = desc
            article_obj.category = category_obj
            article_obj.save()
            tag_list = request.POST.get("tags").strip().split(",")
            tag_list_obj = []
            if tag_list:
                for tag in tag_list:
                    tag_obj = models.Tag.objects.filter(title=tag).first()
                    if tag_obj:
                        tag_obj = tag_obj
                    else:
                        tag_obj = models.Tag.objects.create(title=tag)
                    tag_list_obj.append(tag_obj)  # 重新绑定标签
                for obj in tag_list_obj:
                    models.Article2Tag.objects.create(article=article_obj, tag=obj)
            return redirect("/api/v1/blog/")
        except Exception as e:
            return HttpResponse("呀！好像出错了>_<")


class DeleteArticle(View):
    """
    删除文章
    """
    def get(self, request):
        article_id = int(request.GET.get("id"))
        models.ArticleDetail.objects.filter(article__nid=article_id).delete()
        models.Article.objects.filter(nid=article_id).delete()
        return JsonResponse({"article_id": str(article_id)})


class Top(View):
    """
    文章置顶
    """
    def get(self, request):
        article_id = request.GET.get("article_id")
        ret = {"code": 1000, "msg": ""}
        try:
            models.Top.objects.update_or_create(
                user=request.user, defaults={"article": article_id})
        except Exception as e:
            ret["code"] = 1001
            ret["msg"] = "置顶失败！"
        return JsonResponse(ret)


class ShowContent(View):
    """
    显示文章内容
    """
    def get(self, request):
        article_id = request.GET.get("id")
        article_obj = models.Article.objects.filter(nid=article_id).first()
        comment_obj_list = models.Comment.objects.filter(article__nid=article_id).all()  # 评论列表
        return render(request, "content-show.html", locals())


class Upload(View):
    """
    文章图片上传
    """
    def post(self, request):
        obj = request.FILES.get('upload_img')
        uid = str(uuid.uuid1())
        path = os.path.join(settings.MEDIA_ROOT, 'add_arcticle_img', uid + ".jpg")
        with open(path, 'wb') as f:
            for line in obj:
                f.write(line)
        res = {
            'error': 0,
            'url': '/media/add_arcticle_img/' + uid + ".jpg"
        }
        return HttpResponse(json.dumps(res))


class UpDown(View):
    """
    文章点赞或踩
    """
    def post(self, request):
        """
        提交点赞或踩的响应
        :param request:
        :return:
        """
        article_id = request.POST.get('article_id')
        is_up = json.loads(request.POST.get('is_up'))  # 获取状态
        user = request.user
        respones = {'status': True}
        try:
            models.ArticleUpDown.objects.create(user=user, article_id=article_id, is_up=is_up)
            if is_up:
                models.Article.objects.filter(pk=article_id).update(up_count=F('up_count') + 1)
            else:
                models.Article.objects.filter(pk=article_id).update(down_count=F('down_count') + 1)
        except Exception as e:
            respones['status'] = False
            if is_up:
                respones['warring'] = '你已经推荐过了'
            else:
                respones['warring'] = '你已经反对过了'
        return JsonResponse(respones)


class Comment(View):
    """
    文章评论
    """
    def post(self, request):
        pid = request.POST.get('pid')  # 取父级评论id
        article_id = request.POST.get('article_id')
        content = request.POST.get('content')
        user_pk = request.user.pk
        respones = {}
        if not pid:  # 若自己没有回复其他人，自己直接评论文章
            comment_obj = models.Comment.objects.create(
                article_id=article_id, user_id=user_pk, content=content)
            models.Article.objects.filter(nid=article_id).update(comment_count=F('comment_count') + 1)
        else:
            comment_obj = models.Comment.objects.create(
                article_id=article_id, user_id=user_pk, content=content, parent_comment_id=pid)
        respones['content'] = comment_obj.content
        respones['create_time'] = comment_obj.create_time
        respones['username'] = comment_obj.user.username
        return JsonResponse(respones)


