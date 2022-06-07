#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2022-06-07 10:27:31
# @Author      : junsircoding
# @File        : comment/admin.py
# @Info        : 
# @Last Edited : 2022-06-07 14:52:52

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
