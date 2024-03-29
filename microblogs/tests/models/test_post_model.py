"""Unit tests of the Post model"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from microblogs.models import Post, User

class PostModelTestCase(TestCase):
    """Unit tests of the Post model"""

    fixtures = ['microblogs/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@ChazzaB')

        self.post = Post(
        author = self.user,
        text = 'This is a post by Chazza Bozza'
        )

    def test_valid_message(self):
        try:
            self.post.full_clean()
        except ValidationError:
            self.fail("Test message should be valid")

    def test_author_must_not_be_blank(self):
        self.post.author = None
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_text_must_not_be_blank(self):
        self.post.text = ''
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    def test_text_must_not_be_overlong(self):
        self.post.text = 'x' * 281
        with self.assertRaises(ValidationError):
            self.post.full_clean()

    #def test_user_can_have_multiple_posts(self):
