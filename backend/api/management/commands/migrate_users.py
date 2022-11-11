from django.core.management.base import BaseCommand
from api.models import UserSentence
from users.models import User
from api.helpers import console
from datetime import date


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        console.info('--------------------------------')
        console.info('      MIGRATE USER INIT         ')
        console.info('--------------------------------')

        console.info('Creating test user...')
        user = User(
            id=1,
            username='test',
            email='test@fake.com',
            password='123456'
        )

        user.save()

        console.info('Creating user sentences...')

        UserSentence(
            type=0,
            origin=0,          
            sentence='hang out',
            meaning='hang out with friends',
            last_time_used=date.today(),
            user=user
        ).save()

        UserSentence(
            type=0,
            origin=0,
            sentence='hurry',
            meaning='meaningX2',
            last_time_used=date.today(),
            user=user
        ).save()

        UserSentence(
            type=0,
            origin=0,
            sentence='spooky',
            meaning='meaningX3',
            last_time_used=date.today(),
            user=user
        ).save()

        UserSentence(
            type=0,
            origin=0,
            sentence='brain',
            meaning='meaningX4',
            last_time_used=date.today(),
            user=user
        ).save()

        UserSentence(
            type=0,
            origin=0,
            sentence='smoke',
            meaning='meaningX5',
            last_time_used=date.today(),
            user=user
        ).save()

        UserSentence(
            type=0,
            origin=0,
            sentence='calm_down',
            meaning='meaningX5',
            last_time_used=date.today(),
            user=user
        ).save()

        console.info('Migration completed successfully')
