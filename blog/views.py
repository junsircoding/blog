#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2022-06-07 10:27:31
# @Author      : junsircoding
# @File        : blog/views.py
# @Info        : 
# @Last Edited : 2022-06-07 14:52:52

from datetime import date
from django.shortcuts import get_object_or_404
from config.models import SideBar
from blog.models import Tag, Post, Category
from django.views.generic import DetailView, ListView
from django.db.models import Q, F
from django.core.cache import cache


class CommonViewMixin:
    """
    通用的视图 Mixin
    """
    def get_context_data(self, **kwargs):
        """
        博客的每个页面都要展示“侧边栏”和“导航”
        于是将这两者的数据放入当前视图函数的上下文
        """
        context = super().get_context_data(**kwargs)
        # 侧边栏数据
        context.update(
            {
                "sidebars": SideBar.get_all(),
            }
        )
        # 导航栏中的类别数据
        context.update(
            Category.get_navs()
        )
        # 导航栏中的标签数据
        context.update(
            {
                "tags":Tag.get_tags()
            }
        )
        return context


class PostDetailView(CommonViewMixin, DetailView):
    """
    博文详情的查询逻辑
    - 继承了 ``CommonViewMixin``, 会返回侧边栏和导航栏数据
    - 此外还要返回博文详情数据
    - 最后渲染到 ``blog/detail.html`` 模板中
    """
    # TODO 检索模型的配置项(~ 表示该类继承的父类), 来自 DetailView ~ BaseDetailView ~ SingleObjectMixin
    queryset = Post.get_all()
    context_object_name = "post" # 这个名称是模板在解析数据时所使用的变量
    pk_url_kwarg = "post_id"

    # TODO 模板渲染的配置项, 来自 DetailView ~ SingleObjectTemplateResponseMixin ~ TemplateResponseMixin
    template_name = "blog/detail.html"

    def get(self, request, *args, **kwargs):
        """
        拓展 get 方法, 加入统计 pv 和 uv 的逻辑
        """
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        # 页面刷新数加 1
        increase_pv = False
        # ip 访问数加 1
        increase_uv = False
        # 当前登录用户唯一 uid
        uid = self.request.uid
        pv_key = f"pv{uid}:{self.request.path}"
        uv_key = f"uv{uid}:{str(date.today())}:{self.request.path}"
        # 新用户访问页面
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60) # 1分钟有效, 防止用户连续刷新页面
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24*60*60) # 24小时有效, 一天之内同一个 IP 只记录一次 UV
        # 更新 pv 和 uv
        current_post = Post.objects.filter(
            pk=self.object.id
        )
        if increase_pv:
            current_post.update(
                pv=F("pv") + 1,
            )
        if increase_uv:
            current_post.update(
                uv=F("uv") + 1,
            )


class IndexView(CommonViewMixin, ListView):
    """
    首页的查询逻辑
    - 继承了 ``CommonViewMixin``, 会返回侧边栏和导航栏数据
    - 此外还要返回博文列表分页数据
    - 最后渲染到 ``blog/list.html`` 模板中
    """
    # TODO 检索模型的配置项(~ 表示该类继承的父类), 来自 DetailView ~ BaseDetailView ~ SingleObjectMixin
    queryset = Post.get_all()
    context_object_name = "post_list"  # 这个名称是模板在解析数据时所使用的变量

    # TODO 操作多个对象视图的配置项, 来自 ListView ~ BaseListView ~ MultipleObjectMixin
    paginate_by = 8
    # TODO 模板渲染的配置项, 来自 ListView ~ MultipleObjectTemplateResponseMixin ~ TemplateResponseMixin
    template_name = "blog/list.html"


class CategoryView(IndexView):
    """
    根据类别 ID 查询博文
    继承自 ``IndexView``, 针对博文进行查询, 即 ``Post`` 模型
    """
    def get_context_data(self, **kwargs):
        """
        拓展了 ``CommonViewMixin`` 的 ``get_context_data`` 方法
        将类别信息加入上下文
        """
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Category, pk=category_id)
        context.update(
            {
                "category": category
            }
        )
        return context

    def get_queryset(self):
        """
        根据类别 ID 查询博文
        """
        queryset = super().get_queryset()
        categroy_id = self.kwargs.get("category_id")
        result = queryset.filter(category=categroy_id)
        return result


class TagView(IndexView):
    """
    根据标签查询博文
    继承自 ``IndexView``, 针对博文进行查询, 即 ``Tag`` 模型
    """
    def get_context_data(self, **kwargs):
        """
        拓展了 ``CommonViewMixin`` 的 ``get_context_data`` 方法
        将标签信息加入上下文
        """
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get("tag_id")
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update(
            {
                "tag": tag
            }
        )
        return context

    def get_queryset(self):
        """
        根据标签 ID 查询博文
        """
        queryset = super().get_queryset()
        tag_id = self.kwargs.get("tag_id")
        return queryset.filter(tag=tag_id)


class SearchView(IndexView):
    """
    关键字筛选博文
    继承自 ``IndexView``, 针对博文进行查询, 即 ``Post`` 模型
    """
    def get_context_data(self, **kwargs):
        """
        拓展了 ``CommonViewMixin`` 的 ``get_context_data`` 方法
        将关键字加入上下文
        """
        context = super().get_context_data()
        context.update(
            {
                "keyword": self.request.GET.get(
                    "keyword",
                    ""
                )
            }
        )
        return context

    def get_queryset(self):
        """
        根据关键字筛选博文
        标题包含关键字或摘要包含关键字
        """
        queryset = super().get_queryset()
        keyword = self.request.GET.get("keyword")
        if not keyword:
            return queryset
        return queryset.filter(
            Q(
                title__icontains=keyword
            )
            |
            Q(
                desc__icontains=keyword
            )
        )


class AuthorView(IndexView):
    """
    作者筛选博文, 此功能已废弃
    继承自 ``IndexView``, 针对博文进行查询, 即 ``Post`` 模型
    上下文中已包含博文作者信息
    """
    def get_queryset(self):
        """
        根据作者 ID 筛选博文
        """
        queryset = super().get_queryset()
        author_id = self.kwargs.get("owner_id")
        return queryset.filter(
            owner_id=author_id
        )
