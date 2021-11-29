from django.test import TestCase
from django.urls import reverse
from microblogs.models import User

class ShowUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            '@ChazzaB',
            first_name='Chaz',
            last_name='Boz',
            email='ChazBosh@outlook.com',
            password='Password123',
            bio='Ayo this da user Chazza Boz yeeee'
        )
        self.url = reverse('show_user', kwargs={'user_id': self.user.id})

    def test_show_user_url(self):
        self.assertEqual(self.url,f'/user/{self.user.id}')

    def test_get_show_user_with_valid_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, "Chaz Boz")
        self.assertContains(response, "@ChazzaB")

    def test_get_show_user_with_invalid_id(self):
        url = reverse('show_user', kwargs={'user_id': self.user.id+1})
        response = self.client.get(url, follow=True)
        response_url = reverse('user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'user_list.html')
