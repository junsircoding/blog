#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2022-06-07 10:27:31
# @Author      : junsircoding
# @File        : blog/models.py
# @Info        : 
# @Last Edited : 2022-06-07 14:52:52

import mistune
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """
    博文类别
    """
    # 博文状态枚举
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    )

    name = models.CharField(
        max_length=50,
        verbose_name="博文类别名称"
    )
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL,
        choices=STATUS_ITEMS,
        verbose_name="分类状态"
    )
    is_nav = models.BooleanField(
        default=False,
        verbose_name="是否为导航"
    )
    owner = models.ForeignKey(
        User,
        verbose_name="分类作者"
    )
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="分类创建时间"
    )

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        """
        返回标记为导航的类别列表
        :return (list)
        """
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        # 导航类别列表
        nav_categories = []
        # 非导航类别列表
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        return {
            "navs": nav_categories,
            "categories": normal_categories
        }

    class Meta:
        # 较长的名称
        verbose_name = "博文分类"
        verbose_name_plural = "博文分类列表"


class Tag(models.Model):
    # 标签枚举值
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    )

    name = models.CharField(
        max_length=10,
        verbose_name="标签名称"
    )
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL,
        choices=STATUS_ITEMS,
        verbose_name="标签状态"
    )
    owner = models.ForeignKey(
        User,
        verbose_name="标签创建者"
    )
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="标签创建时间"
    )

    @classmethod
    def get_tags(cls):
        tags = cls.objects.filter(status=cls.STATUS_NORMAL)
        return [tag for tag in tags]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "博文标签"
        verbose_name_plural = "博文标签列表"


class Post(models.Model):
    # 博文状态枚举
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
        (STATUS_DRAFT, "草稿"),
    )

    title = models.CharField(
        max_length=255,
        verbose_name="标题"
    )
    desc = models.CharField(
        max_length=1024,
        blank=True,
        verbose_name="摘要"
    )
    content = models.TextField(
        verbose_name="正文",
        help_text="正文必须为MarkDown格式"
    )
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL,
        choices=STATUS_ITEMS,
        verbose_name="状态"
    )
    category = models.ForeignKey(
        Category,
        verbose_name="分类"
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name="标签"
    )
    owner = models.ForeignKey(
        User,
        verbose_name="作者"
    )
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间"
    )
    content_html = models.TextField(
        verbose_name="正文html代码",
        blank=True,
        editable=False
    )

    """
    PV(page view) 页面点击量
    UV(unique visitor) 不同IP地址数量
    PR(PageRank) 被引用次数, 受欢迎程度
    """
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    @property
    def comment_count(self):
        """
        查询文章评论数
        """
        from comment.models import Comment
        return Comment.objects.filter(target=f"/post/{self.id}.html").count

    def __str__(self):
        """
        用str()格式化时显示的内容
        """
        return self.title
    
    def save(self, *args, **kwargs):
        self.content_html = mistune.markdown(self.content)
        super().save( *args, **kwargs)

    @staticmethod
    def get_by_tag(tag_id):
        """
        根据标签筛选博文
        :param tag_id (int)
        :return Tuple[list, int]
        """
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(
                status=Post.STATUS_NORMAL
            ).select_related(
                "owner",
                "tag"
            )
        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        """
        根据类别筛选博文
        :param category_id (int)
        :return Tuple[list, int]
        """
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(
                status=Post.STATUS_NORMAL
            ).select_related(
                "owner",
                "category"
            )
        return post_list, category

    @classmethod
    def hot_posts(cls):
        """
        热门文章,按照pv倒序排列
        :param cls (object)
        :return (object)
        """
        return cls.objects.filter(
            status=cls.STATUS_NORMAL
        ).order_by("-pv")[0:3]

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(
            status=cls.STATUS_NORMAL
        ).order_by("-created_time")
        return queryset[0:3]

    @classmethod
    def get_all(cls):
        queryset = cls.objects.filter(
            status=cls.STATUS_NORMAL
        )
        return queryset

    class Meta:
        verbose_name = "博文"
        verbose_name_plural = "博文列表"
        ordering = ["-id"]  # 根据ID降序排列
