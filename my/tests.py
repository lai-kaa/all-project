from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from my.models import Order
from ticket.models import Train, Seat
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


class AuthTests(TestCase):
    """用户注册与登录测试"""

    def setUp(self):
        self.client = Client()

    def test_register_with_simple_password(self):
        """允许简单密码（如纯数字、短密码）"""
        response = self.client.post(reverse('register'), {
            'username': 'simpleuser',
            'password1': '123',
            'password2': '123',
        })
        self.assertRedirects(response, reverse('my_orders'))
        user = User.objects.get(username='simpleuser')
        self.assertTrue(user.check_password('123'))

    def test_register_and_login(self):
        """注册成功后跳转订单页"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertRedirects(response, reverse('my_orders'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_my_orders_requires_login(self):
        """订单页需要登录"""
        response = self.client.get(reverse('my_orders'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_user_cannot_refund_others_order(self):
        """用户不能退他人订单"""
        owner = User.objects.create_user(username='owner', password='pass12345')
        other = User.objects.create_user(username='other', password='pass12345')
        train = Train.objects.create(
            number='D2002',
            train_type='D',
            qi='杭州',
            mudi='南京',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
        )
        seat = Seat.objects.create(
            train=train,
            type='first',
            price=Decimal('200.00'),
            number=5,
        )
        order = Order.objects.create(
            user=owner,
            train=train,
            seat=seat,
            price=seat.price,
        )

        self.client.login(username='other', password='pass12345')
        response = self.client.post(reverse('refund_ticket', args=[order.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Order.objects.filter(id=order.id).exists())
