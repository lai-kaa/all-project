from unittest.mock import patch

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class SupportViewTests(TestCase):
    """智能客服页面测试"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('support')

    def test_support_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '智能客服')

    @patch('support.views.ask_deepseek')
    def test_support_post_with_mock(self, mock_ask):
        mock_ask.return_value = '您可以登录后在车票页面购买。'
        response = self.client.post(self.url, {'question': '如何购票？'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '您可以登录后在车票页面购买')
        self.assertContains(response, 'qq-bubble-user')
        self.assertContains(response, 'qq-bubble-bot')
        mock_ask.assert_called_once_with('如何购票？')


class PasswordTests(TestCase):
    """忘记密码与修改密码"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='OldPass123!',
        )

    def test_forgot_password_page(self):
        response = self.client.get(reverse('forgot_password'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '忘记密码')
        self.assertNotContains(response, '邮箱')
        self.assertNotContains(response, '邮件')

    def test_forgot_password_reset_directly(self):
        """用户名 + 新密码直接重置"""
        response = self.client.post(reverse('forgot_password'), {
            'username': 'tester',
            'new_password1': 'NewPass789!',
            'new_password2': 'NewPass789!',
        })
        self.assertRedirects(response, reverse('forgot_password_done'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass789!'))

    def test_forgot_password_done_page(self):
        response = self.client.get(reverse('forgot_password_done'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '密码重置成功')

    def test_change_password_requires_login(self):
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_change_password_no_old_password_field(self):
        """修改密码页不应出现旧密码输入框"""
        self.client.login(username='tester', password='OldPass123!')
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'old_password')
        self.assertNotContains(response, 'name="old_password"')
        self.assertContains(response, 'new_password1')
        self.assertContains(response, 'new_password2')

    def test_change_password_success(self):
        """已登录用户可直接修改密码，无需旧密码"""
        self.client.login(username='tester', password='OldPass123!')
        response = self.client.post(reverse('password_change'), {
            'new_password1': 'NewPass456!',
            'new_password2': 'NewPass456!',
        })
        self.assertRedirects(response, reverse('password_change_done'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass456!'))
