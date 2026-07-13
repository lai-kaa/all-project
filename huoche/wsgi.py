"""
WSGI 入口，供 gunicorn / uWSGI 等生产服务器调用。
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huoche.settings')

application = get_wsgi_application()
