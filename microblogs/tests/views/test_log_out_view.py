"""Tests of the log out view"""
from django.test import TestCase
from django.urls import reverse
from microblogs.models import User
from microblogs.tests.helpers import LogInTester

class LogOutViewTestCase(TestCase, LogInTester):
    """Tests of the log out view"""

    def setUp(self):
        self.url = reverse('log_out')
        self.user = User.objects.create_user(
            '@ChazzaB',
            first_name='Chaz',
            last_name='Boz',
            email='ChazBosh@outlook.com',
            password='Password123',
            bio='Ayo this da user Chazza Boz yeeee',
            is_active=True
        )

    def test_log_out_url(self):
        self.assertEqual(self.url, '/log_out/')

    def test_get_log_out(self):
        self.client.login(username='@ChazzaB', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertFalse(self._is_logged_in())
