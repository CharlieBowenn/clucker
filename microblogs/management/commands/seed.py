from django.core.management.base import BaseCommand, CommandError
from clucker.microblogs import User
from faker import Faker

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        fake = Faker()
        list=[]
        for x in range(0, 99):
            firstName = fake.first_name()
            lastName = fake.last_name()
            username = '@'+firstName+lastName
            email = firstName+'.'+lastName+'@outlook.com'
            bio = 'Hi my name is '+firstName
            first = User(username, firstName, lastName, email, bio)
            list.append(first)

        for x in range(0, len(list)):
            print(list[x].username)
