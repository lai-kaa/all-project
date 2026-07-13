from django.urls import path

from . import views

# 用户相关路由（注册 / 登录 / 订单 / 密码 / 退票）
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my/', views.my_orders, name='my_orders'),
    path('refund/<int:order_id>/', views.refund_ticket, name='refund_ticket'),

    # 忘记密码：用户名 + 新密码直接重置
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('forgot-password/done/', views.forgot_password_done_view, name='forgot_password_done'),

    # 已登录用户直接修改密码（无需旧密码）
    path('change-password/', views.change_password_view, name='password_change'),
    path('change-password/done/', views.change_password_done_view, name='password_change_done'),
]
