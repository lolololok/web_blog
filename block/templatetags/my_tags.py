from django import template
from block import models
from django.db.models import Count

register = template.Library()

# 左侧数据显示
@register.inclusion_tag('left-nav.html')
def get_left_menu(request):
    """
    左侧导航条信息显示
    :param request:
    :return:
    """
    return locals()


# 右侧数据显示
@register.inclusion_tag('right-nav.html')
def get_right_menu(request):
    """
    右侧导航条信息显示
    :param request:
    :return:
    """
    category_list = models.Category.objects.filter(
        article__user=request.user
    ).annotate(c=Count('article')).values('title', 'c', "nid")
    tag_list = models.Tag.objects.filter(
        article__user=request.user
    ).annotate(c=Count('article')).values('title', 'c', "nid")
    # 按日期归档
    archive_list = models.Article.objects.filter(user=request.user).extra(
        select={'ym': 'date_format(create_time,"%%Y-%%m")'}  # 只选出月和年
    ).values('ym').annotate(c=Count('nid')).values('ym', 'c')
    return locals()
