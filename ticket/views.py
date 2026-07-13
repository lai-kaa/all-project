from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from django.db import transaction
from django.utils import timezone
from datetime import datetime

from huoche.search_utils import filter_trains_by_keyword
from my.models import Order
from .models import Train, Seat


def ticket(request):
    """
    车票查询页：支持顶部关键词模糊搜索，以及出发地/目的地/日期精确筛选。
    使用 prefetch_related 减少查询次数。
    """
    trains = Train.objects.prefetch_related('seats').all()

    # 顶部搜索框关键词
    q = request.GET.get('q', '').strip()
    # 下方筛选表单参数
    qi = request.GET.get('qi', '').strip()
    mudi = request.GET.get('mudi', '').strip()
    date_str = request.GET.get('date', '').strip()

    if q:
        trains = filter_trains_by_keyword(trains, q)
    if qi:
        trains = trains.filter(qi__icontains=qi)
    if mudi:
        trains = trains.filter(mudi__icontains=mudi)
    if date_str:
        try:
            query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            trains = trains.filter(start_time__date=query_date)
        except ValueError:
            messages.warning(request, '日期格式无效，请使用 YYYY-MM-DD')

    context = {
        'trains': trains,
        'q': q,
        'qi': qi,
        'mudi': mudi,
        'date': date_str,
        'today': timezone.localdate().isoformat(),
    }
    return render(request, 'ticket.html', context)


@login_required
@transaction.atomic
def buy_ticket(request):
    """
    购票接口：仅接受 POST。
    价格在服务端从 Seat 读取，不信任前端传值。
    使用 select_for_update 防止并发超卖。
    """
    if request.method != 'POST':
        return redirect('ticket')

    train_number = request.POST.get('train')
    seat_type = request.POST.get('seat')

    if not train_number or not seat_type:
        messages.error(request, '购票参数不完整，请重试')
        return redirect('ticket')

    train = get_object_or_404(Train, number=train_number)
    # 锁定座位行，避免并发购票时余票计算错误
    seat = get_object_or_404(
        Seat.objects.select_for_update(),
        train=train,
        type=seat_type,
    )

    if seat.number <= 0:
        messages.error(request, '抱歉，该座位类型已售罄！')
        return redirect('ticket')

    # 使用 F 表达式原子扣减余票
    updated = Seat.objects.filter(pk=seat.pk, number__gt=0).update(
        number=F('number') - 1
    )
    if updated == 0:
        messages.error(request, '抱歉，该座位类型已售罄！')
        return redirect('ticket')

    # 价格始终取自数据库，防止客户端篡改
    Order.objects.create(
        user=request.user,
        train=train,
        seat=seat,
        price=seat.price,
    )

    messages.success(request, '购买成功！')
    return redirect('my_orders')
