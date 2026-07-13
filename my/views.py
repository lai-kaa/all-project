from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import RegisterForm, DirectPasswordChangeForm, ForgotPasswordForm
from .models import Order
from ticket.models import Seat


def register_view(request):
    """用户注册：成功后自动登录并跳转订单页"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册成功，欢迎购票！')
            return redirect('my_orders')
        return render(request, 'register.html', {'form': form})

    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """用户登录：支持 next 参数跳回购票前页面"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # 仅允许跳转到本站路径，防止开放重定向
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect('my_orders')
        return render(request, 'login.html', {'form': form})

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """用户登出"""
    logout(request)
    messages.info(request, '您已安全退出')
    return redirect('login')


@login_required
def my_orders(request):
    """我的订单：按购买时间倒序展示"""
    orders = (
        Order.objects.filter(user=request.user)
        .select_related('train', 'seat')
        .order_by('-created_at')
    )
    return render(request, 'index_my.html', {'orders': orders})


@login_required
@require_POST
@transaction.atomic
def refund_ticket(request, order_id):
    """
    退票：仅允许 POST，防止 GET 误触发。
    在事务中恢复余票并删除订单，保证数据一致。
    """
    order = get_object_or_404(
        Order.objects.select_related('seat'),
        id=order_id,
        user=request.user,
    )

    # 锁定座位行后恢复余票
    seat = Seat.objects.select_for_update().get(pk=order.seat_id)
    Seat.objects.filter(pk=seat.pk).update(number=F('number') + 1)

    order.delete()

    messages.success(request, '退票成功！')
    return redirect('my_orders')


@login_required
def change_password_view(request):
    """
    已登录用户直接修改密码。
    只需填写新密码，无需验证旧密码。
    """
    if request.method == 'POST':
        form = DirectPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 保持登录状态，避免改密后被登出
            update_session_auth_hash(request, user)
            messages.success(request, '密码修改成功！')
            return redirect('password_change_done')
    else:
        form = DirectPasswordChangeForm(request.user)

    return render(request, 'registration/password_change_form.html', {'form': form})


@login_required
def change_password_done_view(request):
    """密码修改成功页"""
    return render(request, 'registration/password_change_done.html')


def forgot_password_view(request):
    """忘记密码：输入用户名和新密码，确认后直接重置"""
    if request.user.is_authenticated:
        messages.info(request, '您已登录，可直接修改密码')
        return redirect('password_change')

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            return redirect('forgot_password_done')
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password.html', {'form': form})


def forgot_password_done_view(request):
    """忘记密码重置成功页"""
    return render(request, 'forgot_password_done.html')