#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2022-06-07 10:27:31
# @Author      : junsircoding
# @File        : manage.py
# @Info        : 
# @Last Edited : 2022-06-07 14:52:52

import os
import sys
if __name__ == "__main__":
    # 将项目配置文件加入环境变量
    profile = os.environ.get(
        "JUNSIRCODING_PROFILE",
        "settings"
    )
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        f"junsircoding.settings.{profile}"
    )
    # 运行环境校验
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django
        except ImportError:
            raise ImportError("无法导入django, 请检查环境")
        raise
    # 执行命令
    execute_from_command_line(sys.argv)
