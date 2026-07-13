"""
全站搜索工具：车次模糊查询 + 公告检索。
"""
from django.db.models import Q

from ticket.models import Train

# 列车类型中文关键词 -> 数据库代码
TRAIN_TYPE_KEYWORDS = {
    '高铁': 'G',
    '动车': 'D',
    '特快': 'T',
    'G': 'G',
    'D': 'D',
    'T': 'T',
}


def filter_trains_by_keyword(queryset, keyword):
    """
    模糊查询车次：匹配车次号、出发地、目的地、列车类型。
    """
    if not keyword:
        return queryset

    conditions = (
        Q(number__icontains=keyword)
        | Q(qi__icontains=keyword)
        | Q(mudi__icontains=keyword)
    )

    for label, code in TRAIN_TYPE_KEYWORDS.items():
        if label.lower() in keyword.lower() or keyword.lower() in label.lower():
            conditions |= Q(train_type=code)

    return queryset.filter(conditions).distinct()


def search_trains(keyword):
    """搜索车次并预加载座位信息"""
    queryset = Train.objects.prefetch_related('seats').all()
    return filter_trains_by_keyword(queryset, keyword)
