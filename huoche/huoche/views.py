from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from django.views.static import serve
from pathlib import Path

def index(request):
    return render(request, 'index.html')

def html_static(request, filename):
    # 只允许 .html 文件，防止目录遍历
    if not filename.endswith('.html'):
        raise Http404
    full_path = Path(settings.BASE_DIR) / 'static' / 'html' / filename
    if not full_path.exists():
        raise Http404
    return serve(request, str(full_path), document_root='/')

 