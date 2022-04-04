# -*- coding:utf-8 -*-
"""
:Date: 2021-07-23 21:48:13
:LastEditTime: 2021-07-23 21:48:13
:Description: 全局配置文件
"""
import os

# manage.py 同级目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 项目密钥
SECRET_KEY = '14^-bhlqhdidy7a1_e0vni+9(5k8c@*o+f44&oapdc-kh(_$#i'

# 调试模式为打开
DEBUG = True

# 允许本项目以何域名被访问
ALLOWED_HOSTS = [
    "127.0.0.1",
]

# 模块
INSTALLED_APPS = [
    "junsircoding",
    # 包含博文、分类等信息
    "blog",
    # 包含友链等信息
    "config",
    # 包含评论信息
    "comment",
    # admin 主题插件
    "grappelli",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# 中间件
MIDDLEWARE = [
    # 中间件：生成用户 uid
    'blog.middleware.user_id.UserIdMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 总路由的路径, blog 模块的 urls 文件
ROOT_URLCONF = 'junsircoding.urls'

# 页面主题切换
THEME = 'bootstrap'

# 模板
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'themes', THEME, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 实现了 wsgi 协议的应用函数
# junsircoding 模块的 wsgi 文件的 application 函数
WSGI_APPLICATION = 'junsircoding.wsgi.application'

# 数据库
# 测试库为 sqlite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 用户密码校验规则
AUTH_PASSWORD_VALIDATORS = [
    # 和用户名不能太相似
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # 不能太短
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # 通用的密码拼接校验
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    # 必须含数字
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 系统语言, 简体中文, hans 中的 s 使 simple, 繁体中文为 zh-hant
LANGUAGE_CODE = 'zh-hans'

# 时区为上海
TIME_ZONE = 'Asia/Shanghai'

# 国际化
USE_I18N = True

# 本地化
USE_L10N = True

USE_TZ = True

# 静态文件目录
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "themes", THEME, "static")
]

# python manage.py collectstatic 命令将静态文件收集到这个目录下
STATIC_ROOT = "/root/junsirblog_statics/static/"

# grappelli 后台标题
GRAPPELLI_ADMIN_TITLE = "junsircoding后台管理"

# 缓存配置
# redis 的版本需要为 2.10.6
CACHES = {
    "default":{
        "BACKEND":"django_redis.cache.RedisCache",
        "LOCATION":"redis://127.0.0.1:6379/1",
        "TIMEOUT":300,
        "OPTIONS":{
            # "PASSWORD":"", # 默认无密码
            "CLIENT_CLASS":"django_redis.client.DefaultClient",
            "PARSER_CLASS":"redis.connection.HiredisParser",
        },
        "CONNECTION_POOL_CLASS":"redis.connection.BlockingConnectionPool",
    }
}
