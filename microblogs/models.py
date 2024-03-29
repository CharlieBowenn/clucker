from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from libgravatar import Gravatar

class User(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least 3 alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    bio = models.CharField(max_length=520, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followees')

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=100):
        """Return a URL to the user's gravatar"""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        return self.gravatar(size=60)

    def toggle_follow(self, followee):
        """Toggles whether self follows a given user"""
        if followee==self:
            return
            
        if self.is_following(followee):
            self._unfollow(followee)
        else:
            self._follow(followee)

    def _follow(self, user):
        user.followers.add(self)

    def _unfollow(self, user):
        user.followers.remove(self)

    def is_following(self, user):
        """Returns whether self follows given user"""
        return user in self.followees.all()

    def follower_count(self):
        """Number of users following self"""
        return self.followers.count()

    def followee_count(self):
        """Number of users self is following"""
        return self.followees.count()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
