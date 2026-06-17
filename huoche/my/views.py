from django.shortcuts import render,redirect

# 导入用户登录验证登出函数
from django.contrib.auth import login,authenticate,logout
#导入内置的登录认证表单
from django.contrib.auth.forms import AuthenticationForm
#导入自定义的注册表单
from .forms import RegisterForm
#导入装饰器@login_required ,只有已登录的用户才能访问
from django.contrib.auth.decorators import login_required

from .models import Order
from django.contrib import messages
from django.shortcuts import get_object_or_404
from ticket.models import Train, Seat 
#用户注册功能
def register_view(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()#保存用户
            #保存登陆状态，标记已登录
            login(request,user)
            return redirect('my_orders')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request,'register.html',{'form':form})
#用户登录功能
def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()#从表单中获取验证后的user对象
            login(request,user)
            return redirect('my_orders')
    
    else:
        form=AuthenticationForm()
    return render(request,'login.html',{'form':form})
#用户登出功能
def logout_view(request):
    logout(request)
    return redirect('login')
#首页(受到登陆保护的)
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'index_my.html', {'orders': orders})

@login_required
def refund_ticket(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # 座位类型映射
    seat_type_map = {
        '商务座': 'business',
        '一等座': 'first', 
        '二等座': 'second'
    }
    
    # 获取座位类型代码
    seat_code = seat_type_map.get(order.seat_type, '')
    
    if seat_code:
        # 找到对应的座位并增加余票
        try:
            train = Train.objects.get(number=order.train_number)
            seat = Seat.objects.get(train=train, type=seat_code)
            seat.number += 1
            seat.save()
        except (Train.DoesNotExist, Seat.DoesNotExist):
            pass  # 忽略错误，继续删除订单
    
    # 删除订单
    order.delete()
    
    messages.success(request, '退票成功！')
    return redirect('my_orders')