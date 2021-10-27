from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from microblogs.models import User

class Command(BaseCommand):
    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        for user in User.objects.all():
            if user.username != '@admin':
                user.delete()
