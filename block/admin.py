from django.contrib import admin
from block import models

# Register your models here.
# 用户信息表
admin.site.register(models.UserInfo)
# 文章
admin.site.register(models.Article)
# 博客信息
# admin.site.register(models.Blog)
# 标签
admin.site.register(models.Tag)
# 评论表
admin.site.register(models.Comment)
# 个人博客文章分类
admin.site.register(models.Category)
# 点赞表
admin.site.register(models.ArticleUpDown)
# 文章详情表
admin.site.register(models.ArticleDetail)
# 文章和标签的多对多关系表
admin.site.register(models.Article2Tag)
# 置顶
admin.site.register(models.Top)