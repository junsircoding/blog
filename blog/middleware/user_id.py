# -*- coding:utf-8 -*-
"""
:Date: 2021-07-24 11:38:34
:LastEditTime: 2021-07-24 11:38:35
:Description: 生成用户唯一 uuid, 用来标识不同用户
Django 的 middleware 在项目启动时会被初始化, 接受请求之后, 会根据配置中的 MIDDLEWARE 配置顺序调用, 传递 request 作为参数
request 是一个类的实例, 可以动态赋值
"""

import uuid


USER_KEY = "uid"
TEN_YEARS = 60 * 60 * 24 * 365 * 10


class UserIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        为了将一个类实例当做函数调用, 就要实现 __call__ 方法
        """
        uid = self.generate_uid(request)
        # TODO 这里给 request 添加 uid 属性, 后续视图中就可以拿到使用
        request.uid = uid
        response = self.get_response(request)
        # TODO 返回响应时设置 cookie
        response.set_cookie(
            USER_KEY,
            uid,
            max_age=TEN_YEARS,
            httponly=True # 只有在服务端能访问
        )
        return response

    def generate_uid(self, request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid
