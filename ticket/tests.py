from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from ticket.models import Train, Seat
from my.models import Order


class TicketFlowTests(TestCase):
    """购票与退票核心流程测试"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.train = Train.objects.create(
            number='G1001',
            train_type='G',
            qi='北京',
            mudi='上海',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=5),
        )
        self.seat = Seat.objects.create(
            train=self.train,
            type='second',
            price=Decimal('553.00'),
            number=10,
        )

    def test_ticket_search_by_city(self):
        """按出发地/目的地筛选车次"""
        url = reverse('ticket')
        response = self.client.get(url, {'qi': '北京', 'mudi': '上海'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'G1001')

        response = self.client.get(url, {'qi': '广州'})
        self.assertNotContains(response, 'G1001')

    def test_ticket_fuzzy_search_by_keyword(self):
        """顶部关键词模糊搜索：车次号、站点、类型"""
        url = reverse('ticket')

        response = self.client.get(url, {'q': 'G100'})
        self.assertContains(response, 'G1001')

        response = self.client.get(url, {'q': '北京'})
        self.assertContains(response, 'G1001')

        response = self.client.get(url, {'q': '高铁'})
        self.assertContains(response, 'G1001')

        response = self.client.get(url, {'q': '深圳'})
        self.assertNotContains(response, 'G1001')

    def test_buy_ticket_requires_login(self):
        """未登录用户不能直接购票"""
        response = self.client.post(reverse('buy_ticket'), {
            'train': 'G1001',
            'seat': 'second',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_buy_ticket_uses_server_price(self):
        """服务端价格为准，忽略客户端篡改"""
        self.client.login(username='tester', password='pass12345')
        response = self.client.post(reverse('buy_ticket'), {
            'train': 'G1001',
            'seat': 'second',
            'price': '0.01',  # 恶意低价
        })
        self.assertRedirects(response, reverse('my_orders'))

        order = Order.objects.get(user=self.user)
        self.assertEqual(order.price, Decimal('553.00'))
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.number, 9)

    def test_buy_ticket_fails_when_sold_out(self):
        """余票为 0 时不能购票"""
        self.seat.number = 0
        self.seat.save()
        self.client.login(username='tester', password='pass12345')

        response = self.client.post(reverse('buy_ticket'), {
            'train': 'G1001',
            'seat': 'second',
        })
        self.assertRedirects(response, reverse('ticket'))
        self.assertEqual(Order.objects.count(), 0)

    def test_refund_requires_post(self):
        """退票仅允许 POST，GET 应返回 405"""
        self.client.login(username='tester', password='pass12345')
        order = Order.objects.create(
            user=self.user,
            train=self.train,
            seat=self.seat,
            price=self.seat.price,
        )
        self.seat.number = 9
        self.seat.save()

        response = self.client.get(reverse('refund_ticket', args=[order.id]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Order.objects.filter(id=order.id).exists())

    def test_refund_restores_seat_count(self):
        """退票后余票恢复"""
        self.client.login(username='tester', password='pass12345')
        order = Order.objects.create(
            user=self.user,
            train=self.train,
            seat=self.seat,
            price=self.seat.price,
        )
        self.seat.number = 9
        self.seat.save()

        response = self.client.post(reverse('refund_ticket', args=[order.id]))
        self.assertRedirects(response, reverse('my_orders'))
        self.assertFalse(Order.objects.filter(id=order.id).exists())
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.number, 10)
