#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2022-06-07 10:27:31
# @Author      : junsircoding
# @File        : comment/templatetags/comment_block.py
# @Info        : 
# @Last Edited : 2022-06-07 14:52:52

from django import template
from comment.forms import CommentForm
from comment.models import Comment


register = template.Library()

@register.inclusion_tag("comment/block.html")
def comment_block(target):
    return {
        "target":target,
        "comment_form" : CommentForm,
        "comment_list" : Comment.get_by_target(target)
    }
