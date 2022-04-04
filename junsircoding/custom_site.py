# -*- coding:utf-8 -*-
"""
:Date: 2021-07-24 15:03:54
:LastEditTime: 2021-07-24 15:03:54
:Description: 自定义管理后台
"""

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
