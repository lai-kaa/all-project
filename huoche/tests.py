from django.test import TestCase, Client
from django.urls import reverse

from huoche.announcements import search_announcements


class GlobalSearchTests(TestCase):
    """全站搜索：公告正文 + 车次"""

    def setUp(self):
        self.client = Client()

    def test_search_announcements_by_body_content(self):
        """按公告正文关键词模糊搜索"""
        results = search_announcements('候补购票')
        self.assertTrue(any(item['filename'] == '候补.html' for item in results))

        results = search_announcements('电子发票')
        self.assertTrue(any(item['filename'] == '数字化电子发票.html' for item in results))

    def test_search_announcements_by_title(self):
        """按公告标题搜索"""
        results = search_announcements('改签')
        filenames = [item['filename'] for item in results]
        self.assertIn('优化车票改签.html', filenames)

    def test_global_search_page(self):
        """搜索页同时展示公告与车次区域"""
        response = self.client.get(reverse('search'), {'q': '候补'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '候补购票操作说明')
        self.assertContains(response, '相关公告')

    def test_empty_search(self):
        """无关键词时不返回结果"""
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '相关公告（')
