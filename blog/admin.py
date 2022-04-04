# -*- coding:utf-8 -*-
"""
:Date: 2021-07-24 11:38:34
:LastEditTime: 2021-07-24 11:38:35
:Description: Tag 和 Category 的管理后台
"""
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from blog.adminforms import PostAdminForm
from blog.models import Post, Category, Tag
from junsircoding.custom_site import custom_site
from junsircoding.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry


# class CategoryOwnerFilter(admin.SimpleListFilter):
#     """
#     自定义过滤器只展示当前用户分类
#     """
#     title = "分类状态"
#     parameter_name = "category_status"

#     def lookups(self, request, model_admin):
#         return Category.objects.filter(
#             owner=request.user
#         ).values_list(
#             "id",
#             "name"
#         )

#     def queryset(self, request, queryset):
#         category_id = self.value()
#         if category_id:
#             return queryset.filter(
#                 id=self.value()
#             )
#         return queryset

# class PostInline(admin.TabularInline):
#     fields = ("title", "desc",)
#     extra = 1
#     model = Post


@admin.register(Category, site=custom_site)
# @admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    """
    博文分类管理
    """
    # 列表显示时要显示的字段
    list_display = (
        "name",
        "status",
        "is_nav",
        "created_time",
        "owner",
        "post_count",
        "operator",
    )
    # 保存/更新数据时表单提供填写的字段
    fields = (
        "name",
        "status",
        "is_nav",
    )
    search_fields = ["name", ]
    # 在分类遍接页面新增文章
    # inlines = [PostInline,]

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = "博文数量"

    def operator(self, obj):
        return format_html(
            "<a href='{}'>修改<a/>",
            reverse(
                "cus_admin:blog_category_change",
                args=(obj.id,)
            )
        )
    operator.short_description = "操作"

    def save_model(self, request, obj, form, change):
        """
        重写save_model方法
        文章作者限制为当前登录用户
        :param request (object)
        :param obj (object)
        :param form (object)
        :param change (object)
        :return (object)
        """
        obj.owner = request.user
        return super(
            CategoryAdmin,
            self
        ).save_model(
            request,
            obj,
            form,
            change
        )


@admin.register(Tag, site=custom_site)
# @admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = (
        "name",
        "status",
        "created_time",
        "owner",
        "post_count",
        "operator",
    )
    fields = (
        "name",
        "status",
    )

    def operator(self, obj):
        return format_html(
            "<a href='{}'>修改<a/>",
            reverse(
                "cus_admin:blog_tag_change",
                args=(obj.id,)
            )
        )
    operator.short_description = "操作"

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = "博文数量"

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(
            TagAdmin,
            self
        ).save_model(
            request,
            obj,
            form,
            change
        )


@admin.register(Post, site=custom_site)
# @admin.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = (
        "title",
        "desc",
        # "content",
        "status",
        "category",
        "owner",
        "created_time",
        "operator",
        # "post_count",
    )
    # fields = (
    #     "category",
    #     "title",
    #     "desc",
    #     "content",
    #     "status",
    #     "tag",
    # )
    fieldsets = (
        (
            "基础配置",
            {
                "description": "",
                "fields": (
                    "title",
                    "category",
                    "status",
                ),
            }
        ),
        (
            "内容",
            {
                "fields": (
                    "desc",
                    "content"
                ),
            }
        ),
        (
            "额外信息",
            {
                # "classes": ("collapse",),
                "fields": ("tag",),
            }
        ),
    )
    filter_horizontal = ("tag",)
    # filter_vertical = ("tag",)
    list_display_links = []
    # list_filter = ["category", ]
    search_fields = ["title", "category__name"]
    actions_on_top = True
    actions_on_bottom = False
    save_on_top = False

    def operator(self, obj):
        return format_html(
            "<a href='{}'>修改<a/>",
            reverse(
                "cus_admin:blog_post_change",
                args=(obj.id,)
            )
        )
    operator.short_description = "操作"

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(
            PostAdmin,
            self
        ).save_model(
            request,
            obj,
            form,
            change
        )

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(
            owner=request.user
        )

    # class Media:
    #     css = {
    #         "all": (
    #             "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
    #         ),
    #     }
    #     js = (
    #         "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js",
    #     )


@admin.register(LogEntry, site=custom_site)
# @admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        "object_repr",
        "object_id",
        "action_flag",
        "user",
        "change_message"
    ]
