"""
ASGI 入口，供 uvicorn / daphne 等异步服务器调用。
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huoche.settings')

application = get_asgi_application()
