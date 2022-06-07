#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2022-06-07 10:27:31
# @Author      : junsircoding
# @File        : config/views.py
# @Info        : 
# @Last Edited : 2022-06-07 14:52:52

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
