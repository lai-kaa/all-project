"""
公告数据与搜索。
公告 HTML 存放在 static/html/ 目录，此处维护索引便于首页展示与全文检索。
"""
import re
from html import unescape
from pathlib import Path

from django.conf import settings

# 公告索引：与首页列表保持一致
ANNOUNCEMENTS = [
    {
        'filename': '关于第三方平台的公告.html',
        'title': '关于第三方平台的公告',
        'date': '2024-12-11',
    },
    {
        'filename': '优化车票改签.html',
        'title': '关于优化铁路车票改签规则的公告',
        'date': '2024-01-11',
    },
    {
        'filename': '旅客禁止托运.html',
        'title': '铁路旅客禁止、限制携带和托运物品目录',
        'date': '2023-11-30',
    },
    {
        'filename': '公告.html',
        'title': '关于保护旅客合法权益的公告',
        'date': '2022-12-22',
    },
    {
        'filename': '数字化电子发票.html',
        'title': '关于铁路客运推广使用全面数字化的电子发票的公告',
        'date': '2024-11-07',
    },
    {
        'filename': '外国护照.html',
        'title': '外国护照身份核验使用说明',
        'date': '2023-12-13',
    },
    {
        'filename': '候补.html',
        'title': '候补购票操作说明',
        'date': '2024-04-19',
    },
    {
        'filename': '车站起售时间.html',
        'title': '关于铁路车站起售时间的公告',
        'date': '2025-06-06',
    },
    {
        'filename': '呼和浩特.html',
        'title': '中国铁路呼和浩特局集团有限公司关于2025年6月14日至20日加开部分旅客列车的公告',
        'date': '2025-06-06',
    },
    {
        'filename': '上海.html',
        'title': '中国铁路上海局集团有限公司关于2025年6月6日-2025年6月12日增开部分旅客列车的公告',
        'date': '2025-06-05',
    },
]


def _html_dir():
    return Path(settings.BASE_DIR) / 'static' / 'html'


def strip_html(html_text):
    """去掉 HTML 标签与脚本样式，提取纯文本用于模糊搜索"""
    text = re.sub(r'<script[^>]*>.*?</script>', ' ', html_text, flags=re.I | re.S)
    text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.I | re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = unescape(text)
    return re.sub(r'\s+', ' ', text).strip()


def read_announcement_text(filename):
    """读取公告文件正文"""
    file_path = _html_dir() / filename
    if not file_path.exists():
        return ''
    return strip_html(file_path.read_text(encoding='utf-8'))


def make_excerpt(text, keyword, radius=40):
    """生成包含关键词的摘要片段"""
    if not text:
        return ''
    lower_text = text.lower()
    lower_keyword = keyword.lower()
    idx = lower_text.find(lower_keyword)
    if idx == -1:
        snippet = text[: radius * 2]
        return snippet + ('...' if len(text) > len(snippet) else '')

    start = max(0, idx - radius)
    end = min(len(text), idx + len(keyword) + radius)
    snippet = text[start:end]
    if start > 0:
        snippet = '...' + snippet
    if end < len(text):
        snippet = snippet + '...'
    return snippet


def search_announcements(keyword):
    """
    模糊搜索公告：匹配标题、文件名、正文内容。
    返回带摘要的结果列表。
    """
    keyword = keyword.strip()
    if not keyword:
        return []

    results = []
    lower_keyword = keyword.lower()

    for item in ANNOUNCEMENTS:
        filename = item['filename']
        title = item['title']
        body = read_announcement_text(filename)
        filename_stem = Path(filename).stem

        haystack = f'{title} {filename_stem} {body}'.lower()
        if lower_keyword not in haystack:
            continue

        results.append({
            **item,
            'excerpt': make_excerpt(body, keyword),
            'url': f'/static/html/{filename}',
        })

    return results
