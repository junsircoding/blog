# -*- coding:utf-8 -*-
"""
:Date: 2021-07-24 14:53:54
:LastEditTime: 2021-07-24 14:53:55
:Description: 后台管理表单自定义显示形式
"""
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
