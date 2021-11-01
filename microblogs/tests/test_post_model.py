"""Unit tests of the Post model"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from microblogs.models import Post, User

class PostModelTestCase(TestCase):
    """Unit tests of the Post model"""

    def setUp(self):
        self.user = User.objects.create_user(
        '@ChazzaB',
        first_name='Chaz',
        last_name='Boz',
        email='ChazBosh@outlook.com',
        password='Password123',
        bio='Ayo this da user Chazza Boz yeeee'
        )

        self.post = Post(
        author = self.user,
        text = 'This is a post by Chazza Bozza'
        )

    #def test_user_can_have_multiple_posts(self):
