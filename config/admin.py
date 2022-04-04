# -*- coding:utf-8 -*-
"""
:Date: 2021-07-23 22:38:36
:LastEditTime: 2021-07-24 13:45:51
:Description: config模块后台管理
"""
from django.contrib import admin
from config.models import Link, SideBar
from junsircoding.custom_site import custom_site
from junsircoding.base_admin import BaseOwnerAdmin


@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    # 列表显示时要显示的字段
    list_display = (
        "title",
        "href",
        "status",
        "weight",
        "owner",
        "created_time",
    )
    # 保存/更新数据时表单提供填写的字段
    fields = (
        "title",
        "href",
        "status",
        "weight",
    )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(
            LinkAdmin,
            self
        ).save_model(
            request,
            obj,
            form,
            change
        )


@admin.register(SideBar, site=custom_site)
class SideBarAdmin(BaseOwnerAdmin):
    # 后台管理中要展示的字段
    list_display = (
        "title",
        "display_type",
        "content",
        "status",
        "owner",
        "created_time",
    )
    # 后台管理中可编辑的字段
    fields = (
        "title",
        "display_type",
        "content",
        "status",
    )

    def save_model(self, request, obj, form, change):
        """
        重写save方法, 侧边栏所属人默认为当前登录用户
        """
        obj.owner = request.user
        return super(
            SideBarAdmin,
            self
        ).save_model(
            request,
            obj,
            form,
            change
        )
