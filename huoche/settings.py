"""
Django 项目配置。
自动加载 .env（优先）或 .env.example，无需安装 python-decouple。
"""
from pathlib import Path
import os
import sys

from .env_loader import get_env, is_configured, load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# 启动时加载环境变量文件
_loaded_env = load_dotenv(BASE_DIR)
if _loaded_env:
    print(f'[配置] 已加载: {_loaded_env.name}')

config = get_env

# 生产环境务必通过环境变量设置 SECRET_KEY
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-g0@a4*kcm$&c6bj3-lj!#*88m)pf3702_&8x7y59@evgv9ln@0',
)

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ticket',
    'my',
    'support',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'huoche.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'huoche.wsgi.application'

# MySQL 数据库，账号密码建议写入 .env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='huoche'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': config('DB_PASSWORD', default='1234'),
        'HOST': config('DB_HOST', default='127.0.0.1'),
        'PORT': config('DB_PORT', default='3306'),
    }
}

# 运行 manage.py test 时使用 SQLite，避免强依赖 MySQL
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'test_db.sqlite3',
        }
    }

# 不限制密码强度（长度、常见密码、纯数字等均允许）
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'zh-hans'
# 使用上海时区，与 12306 场景一致
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = (BASE_DIR / 'static',)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 未登录用户访问受保护页面时跳转至此
LOGIN_URL = '/login/'

# DeepSeek V4 智能客服（密钥写入 .env）
DEEPSEEK_API_KEY = config('DEEPSEEK_API_KEY', default='') if is_configured('DEEPSEEK_API_KEY') else ''
DEEPSEEK_MODEL = config('DEEPSEEK_MODEL', default='deepseek-v4-flash')
DEEPSEEK_BASE_URL = config('DEEPSEEK_BASE_URL', default='https://api.deepseek.com')
DEEPSEEK_TIMEOUT = config('DEEPSEEK_TIMEOUT', default=30, cast=int)
