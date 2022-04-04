# -*- coding:utf-8 -*-
"""
:Date: 2021-07-23 22:51:35
:LastEditTime: 2021-07-24 13:41:47
:Description: 
"""
from django.contrib import admin
from comment.models import Comment
from junsircoding.custom_site import custom_site



@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    # 列表显示时要显示的字段
    list_display = (
        "target",
        "content",
        "nickname",
        "website",
        "email",
        "status",
        "created_time",
    )
