#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2022-06-07 10:27:31
# @Author      : junsircoding
# @File        : blog/adminforms.py
# @Info        : 
# @Last Edited : 2022-06-07 14:52:52

from django import forms


class PostAdminForm(forms.ModelForm):
    """
    博文详情中的字段展示形式,desc字段改为用textarea组件展示
    """
    desc = forms.CharField(
        widget=forms.Textarea,
        label="摘要",
        required=False
    )
