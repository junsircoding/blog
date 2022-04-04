# -*- coding:utf-8 -*-
"""
:Date: 2021-07-23 21:54:46
:LastEditTime: 2021-07-23 21:54:46
:Description: 实现了 wsgi 协议的 app
"""

import os

from django.core.wsgi import get_wsgi_application
# 将项目配置文件加入环境变量
profile = os.environ.get(
    "JUNSIRCODING_PROFILE",
    # "dev_conf"
    "prod_conf"
)
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"junsircoding.settings.{profile}"
)

application = get_wsgi_application()
