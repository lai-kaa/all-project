
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from django.db import transaction
from my.models import Order
from .models import Train, Seat

def ticket(request):
    trains = Train.objects.prefetch_related('seats').all()
    print("DEBUG: trains count =", trains.count())  
    return render(request, 'ticket.html', {'trains': trains})




@login_required
@transaction.atomic
def buy_ticket(request):
    if request.method == 'POST':
        train_number = request.POST.get('train')
        seat_type = request.POST.get('seat')
        price = request.POST.get('price')

        # 获取列车和座位信息（使用select_for_update锁定行，防止并发问题）
        train = get_object_or_404(Train, number=train_number)
        seat = get_object_or_404(Seat.objects.select_for_update(), train=train, type=seat_type)
        
        # 检查余票是否充足
        if seat.number <= 0:
            messages.error(request, '抱歉，该座位类型已售罄！')
            return redirect('ticket')
        
        # 减少余票数量
        seat.number = seat.number - 1
        seat.save()
        
        # 创建订单
        Order.objects.create(
            user=request.user,
            train_number=train_number,
            seat_type=seat.get_type_display(),
            price=price
        )

        messages.success(request, '购买成功！')
        return redirect('my_orders')