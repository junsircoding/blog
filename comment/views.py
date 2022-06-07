#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2022-06-07 10:27:31
# @Author      : junsircoding
# @File        : comment/views.py
# @Info        : 
# @Last Edited : 2022-06-07 14:52:52

from django.shortcuts import redirect
from django.views.generic import TemplateView
from comment.forms import CommentForm


class CommentView(TemplateView):
    """
    评论模块的视图
    """
    # TODO 可以接受的 HTTP 请求类型, 来自 TemplateView ~ View
    http_method_names = ["post"]

    # TODO 最终数据要渲染到的模板文件, 来自 TemplateView ~ TemplateResponseMixin
    template_name = "comment/result.html"

    # View 类可以根据方法的名称去分发对应的 HTTP 请求 
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get("target")

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)

        else:
            succeed = False

        context = {
            "succeed": succeed,
            "form": comment_form,
            "target": target,
        }
        return self.render_to_response(context)
