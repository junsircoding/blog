# -*- coding:utf-8 -*-
"""
:Date: 2021-07-23 22:11:31
:LastEditTime: 2021-07-23 22:12:27
:Description: 知识库和侧边栏模型
"""
from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string


class Link(models.Model):
    """
    知识库模型
    """
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    )
    title = models.CharField(
        max_length=50,
        verbose_name="标题"
    )
    href = models.URLField(
        verbose_name="链接"
    )  # 默认长度为200
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL,
        choices=STATUS_ITEMS,
        verbose_name="状态"
    )
    weight = models.PositiveIntegerField(
        default=1,
        choices=zip(
            range(1, 6),
            range(1, 6)
        ),
        verbose_name="权重",
        help_text="权重高展示顺序靠前"
    )
    owner = models.ForeignKey(
        User,
        verbose_name="作者"
    )
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间"
    )

    def __str__(self):
        return f"由[{self.owner}]创建的友链[{self.title}]"

    class Meta:
        verbose_name = "知识库"
        verbose_name_plural = "知识库列表"


class SideBar(models.Model):
    """
    侧边栏模型
    """
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, "展示"),
        (STATUS_HIDE, "隐藏"),
    )
    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4
    SIDE_TYPE = (
        (DISPLAY_HTML, "HTML"),
        (DISPLAY_LATEST, "最新三篇文章"),
        (DISPLAY_HOT, "最热三篇文章"),
        (DISPLAY_COMMENT, "最近三条评论"),
    )
    title = models.CharField(
        max_length=50,
        verbose_name="标题"
    )
    display_type = models.PositiveIntegerField(
        default=DISPLAY_HTML,
        choices=SIDE_TYPE,
        verbose_name="展示类型"
    )
    content = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="内容",
        help_text="如果设置的不是HTML类型, 可为空"
    )
    status = models.PositiveIntegerField(
        default=STATUS_SHOW,
        choices=STATUS_ITEMS,
        verbose_name="状态"
    )
    owner = models.ForeignKey(
        User,
        verbose_name="作者"
    )
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间"
    )

    @property
    def content_html(self):
        """
        直接渲染模板
        """
        from blog.models import Post
        from comment.models import Comment

        result = ""
        if self.display_type == self.DISPLAY_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:
            """
            最新三篇文章
            """
            context = {
                "posts": Post.latest_posts()
            }
            result = render_to_string(
                "config/blocks/sidebar_posts.html",
                context
            )
        elif self.display_type == self.DISPLAY_HOT:
            """
            最热三篇文章
            """
            context = {
                "posts": Post.hot_posts()
            }
            result = render_to_string(
                "config/blocks/sidebar_posts.html",
                context
            )
        elif self.display_type == self.DISPLAY_COMMENT:
            """
            最新三条评论
            """
            context = {
                "comments": Comment.latest_comments()
            }
            result = render_to_string(
                "config/blocks/sidebar_comments.html",
                context
            )
        return result

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls):
        return cls.objects.filter(
            status=cls.STATUS_SHOW
        )

    class Meta:
        verbose_name = "侧边栏"
        verbose_name_plural = "侧边栏列表"
