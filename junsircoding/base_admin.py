#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2022-06-07 10:27:31
# @Author      : junsircoding
# @File        : junsircoding/base_admin.py
# @Info        : 
# @Last Edited : 2022-06-07 14:52:52

from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    exclude = ("owner",)

    def get_queryset(self, request):
        qs = super(
            BaseOwnerAdmin,
            self
        ).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(
            BaseOwnerAdmin,
            self).save_model(
                request,
                obj,
                form,
                change
        )
