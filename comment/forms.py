#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2022-06-07 10:27:31
# @Author      : junsircoding
# @File        : comment/forms.py
# @Info        : 
# @Last Edited : 2022-06-07 14:52:52

import mistune
from django import forms
from comment.models import Comment


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label="昵称",
        max_length=50,
        label_suffix="（必填, 你的昵称将显示给所有人看）",
        widget=forms.widgets.Input(
            attrs={
                "class": "form-control",
                "style": "width:60%;"
            }
        )
    )
    email = forms.CharField(
        label="Email",
        label_suffix="（必填, 你的邮箱不会公开显示）",
        max_length=50,
        widget=forms.widgets.EmailInput(
            attrs={
                "class": "form-control",
                "style": "width: 60%;"
            }
        )
    )
    website = forms.CharField(
        label="个人网站",
        label_suffix="（必填, 其他人点击你的昵称会直接访问你的网站, 请勿填写广告！）",
        max_length=100,
        widget=forms.widgets.URLInput(
            attrs={
                "class": "form-control",
                "style": "width: 60%;",
                "value":"https://"
            }
        )
    )
    content = forms.CharField(
        label="内容",
        label_suffix="（必填, 支持 Markdown, 请友善评论）",
        max_length=1000,
        widget=forms.widgets.Textarea(
            attrs={
                "rows": 6,
                "cols": 60,
                "class": "form-control"
            }
        )
    )
    def clean_content(self):
        content = self.cleaned_data.get("content")
        # if len(content) < 10:
        #     raise forms.ValidationError("内容长度过短")
        content = mistune.markdown(content)
        return content
    class Meta:
        model = Comment
        fields = [
            "nickname",
            "email",
            "website",
            "content",
        ]
