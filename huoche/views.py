from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from django.views.static import serve
from django.utils import timezone
from pathlib import Path

from .announcements import search_announcements
from .search_utils import search_trains


def index(request):
    """12306 风格首页：轮播图与公告入口"""
    return render(request, 'index.html')


def global_search(request):
    """
    全站搜索：同时检索车次与公告正文。
    顶部搜索框提交到此页面。
    """
    q = request.GET.get('q', '').strip()
    trains = search_trains(q) if q else []
    announcements = search_announcements(q) if q else []

    context = {
        'q': q,
        'trains': trains,
        'announcements': announcements,
        'today': timezone.localdate().isoformat(),
        'result_count': len(trains) + len(announcements),
    }
    return render(request, 'search.html', context)


def html_static(request, filename):
    """
    提供 static/html 下的公告页面。
    仅允许 .html 后缀，防止目录遍历攻击。
    """
    if not filename.endswith('.html'):
        raise Http404
    full_path = Path(settings.BASE_DIR) / 'static' / 'html' / filename
    if not full_path.exists():
        raise Http404
    return serve(request, str(full_path), document_root='/')
