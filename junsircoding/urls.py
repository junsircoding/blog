#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2022-06-07 10:27:31
# @Author      : junsircoding
# @File        : junsircoding/urls.py
# @Info        : 
# @Last Edited : 2022-06-07 14:52:52

from django.conf.urls import url, include
from blog.views import (
    IndexView, CategoryView,
    TagView, PostDetailView,
    SearchView, AuthorView
)
from config.views import LinkListView
from comment.views import CommentView
from junsircoding.custom_site import custom_site


urlpatterns = [
    # 评论
    url(
        r"^comment/$",
        CommentView.as_view(),
        name="comment"
    ),
    # 友链
    url(
        r"^links/$",
        LinkListView.as_view(),
        name="links"
    ),
    # 作者页面
    url(
        r"author/(?P<owner_id>\d+)/$",
        AuthorView.as_view(),
        name="author"
    ),
    # 首页搜索
    url(
        r"^search/$",
        SearchView.as_view(),
        name="search"
    ),
    # 首页,http://127.0.0.1:8000/
    url(
        r'^$',
        IndexView.as_view(),
        name="index"
    ),
    # 根据类别筛选文章,http://127.0.0.1:8000/category/2/
    url(
        r'^category/(?P<category_id>\d+)/$',
        CategoryView.as_view(),
        name="category-list"
    ),
    # 根据标签筛选文章,http://127.0.0.1:8000/tag/2/
    url(
        r'^tag/(?P<tag_id>\d+)/$',
        TagView.as_view(),
        name="tag-list"
    ),
    # 文章详情,http://127.0.0.1:8000/post/2.html
    url(
        r'^post/(?P<post_id>\d+).html$',
        PostDetailView.as_view(),
        name="post-detail"
    ),
    # 后台主题 grappelli
    url(r'^grappelli/', include('grappelli.urls')),
    # 系统后台管理,http://127.0.0.1:8000/junsiradmin/
    url(
        r'^junsiradmin/',
        custom_site.urls,
        name="admin"
    ),
]
