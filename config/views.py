# -*- coding:utf-8 -*-
"""
:Date: 2021-07-23 22:38:36
:LastEditTime: 2021-07-24 15:42:36
:Description: config APP 的视图函数, 侧边栏的逻辑已在通用视图中包含, 这里不再写侧边栏的查询逻辑
"""

from blog.views import CommonViewMixin
from config.models import Link
from django.views.generic import ListView


class LinkListView(CommonViewMixin, ListView):
    """
    查询所有友链, 将结果渲染到 ``config/links.html``
    """
    queryset = Link.objects.filter(
        status=Link.STATUS_NORMAL
    )
    template_name = "config/links.html"
    context_object_name = "link_list"

    paginate_by = 8
    