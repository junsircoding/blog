#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2022-06-07 10:27:31
# @Author      : junsircoding
# @File        : junsircoding/wsgi.py
# @Info        : 
# @Last Edited : 2022-06-07 14:52:52

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
