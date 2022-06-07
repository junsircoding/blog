#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2022-06-07 10:27:31
# @Author      : junsircoding
# @File        : junsircoding/custom_site.py
# @Info        : 
# @Last Edited : 2022-06-07 14:52:52

from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    # 网页页头
    site_header = "junsircoding 管理"
    # 浏览器标签显示文案
    site_title = "后台管理"
    # 网页标题
    index_title = "模块总览"


# 实例化自定义后台,供路由表调用视图
custom_site = CustomSite(
    name="cus_admin"
)
