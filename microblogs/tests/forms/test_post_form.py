from django.test import TestCase
from microblogs.models import User, Post
from microblogs.forms import PostForm

class PostFormTestCase(TestCase):
    def setUp(self):
        super(TestCase, self).sestUp()
        self.user = User.objects.create_user(
            '@ChazzaB',
            first_name='Chaz',
            last_name='Boz',
            email='ChazBosh@outlook.com',
            password='Password123',
            bio='Ayo this da user Chazza Boz yeeee'
        )

    def test_valid_post_form(self):
        input = {'text': 'x'*200 }
        form = PostForm(data=input)
        self.assertTrue(form.is_valid())

    def test_invalid_post_form(self):
        input = {'text': 'x'*600 }
        form = PostForm(data=input)
        self.assertFalse(form.is_valid())
