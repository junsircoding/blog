# -*- coding:utf-8 -*-
"""
:Date: 2021-07-23 22:11:31
:LastEditTime: 2021-07-23 22:12:27
:Description: 
"""
from blog.models import Post
from django.db import models


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    )

    target = models.CharField(
        max_length=100,
        verbose_name="评论目标"
    )
    content = models.CharField(
        max_length=2000,
        verbose_name="内容"
    )
    nickname = models.CharField(
        max_length=50,
        verbose_name="昵称"
    )
    website = models.URLField(
        verbose_name="网站"
    )
    email = models.EmailField(
        verbose_name="邮箱"
    )
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL,
        choices=STATUS_ITEMS,
        verbose_name="状态"
    )
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间"
    )

    def __str__(self):
        return f"[{self.nickname}]对[{self.target}]的评论"

    @classmethod
    def get_by_target(cls, target):
        return cls.objects.filter(
            target=target,
            status=cls.STATUS_NORMAL
        )

    @classmethod
    def latest_comments(cls):
        return cls.objects.filter(
            status=Comment.STATUS_NORMAL
            ).order_by("-created_time")[0:3]

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论列表"
