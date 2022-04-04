# -*- coding:utf-8 -*-
"""
:Date: 2021-07-27 19:13:56
:LastEditTime: 2021-07-27 19:13:56
:Description: 
"""

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
