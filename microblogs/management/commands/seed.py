from django.core.management.base import BaseCommand, CommandError
from microblogs.models import User
from faker import Faker

class Command(BaseCommand):
    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        for x in range(0, 99):
            firstName = self.faker.first_name()
            lastName = self.faker.last_name()
            username = '@'+firstName+lastName
            email = firstName+'.'+lastName+'@outlook.com'
            bio = 'Hi my name is '+firstName
            addUser = User.objects.create_user(
            username = username,
            first_name = firstName,
            last_name = lastName,
            email = email,
            bio = bio
            )
            addUser.save()
