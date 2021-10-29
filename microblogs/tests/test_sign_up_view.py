"""Tests of the sign up view"""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from microblogs.forms import SignUpForm
from microblogs.models import User

class SignUpViewTestCase(TestCase):
    """Tests of the sign up view"""

    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'username': '@janedoe',
        'email': 'janedoe@example.org',
        'bio': 'YO YOOOOO dis ma bio',
        'new_password': 'Password123',
        'password_confirmation': 'Password123'
        }

    # reverse function obtains url from the path in urls.py
    def test_sign_up_url(self):
        self.assertEqual(self.url, '/sign_up/')

    # Makes get request to sign up page
    # If request successful, response should include status code 200 (OK)
    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        # context is variable containing form used
        # use 'form' as this is name used in sign up view --> {'form': form}
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_unsuccesful_sign_up(self):
        self.form_input['username'] = 'BAD_USER_NAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)

    def test_succesful_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        user = User.objects.get(username='@janedoe')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
        self.assertEqual(user.bio, 'YO YOOOOO dis ma bio')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
