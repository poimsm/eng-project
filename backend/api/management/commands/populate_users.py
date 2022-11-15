from django.core.management.base import BaseCommand
from api.models import (
    UserSentence, ResourceSentence, ShortVideo, InfoCard,
    WordOrigin, WordTypes, SourceTypes
)
from users.models import User
from api.helpers import console
from datetime import date


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        console.info('--------------------------------')
        console.info('    POPULATE USER               ')
        console.info('--------------------------------')

        console.info('Creating fake user...')
        user = User(
            id=1,
            username='test',
            email='test@fake.com',
            password='123456'
        )
        
        user.save()

        console.info('Adding user-entered sentences...')

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

        # --------------------------VIDEO---------------------------------------------
        console.info('Adding videos to user favorites...')
        video_obj = ShortVideo.objects.get(id=1)
        sentence_obj = ResourceSentence.objects.filter(
            short_video=video_obj.id)

        for sen in sentence_obj:
            UserSentence(
                sentence=sen.sentence,
                meaning=sen.meaning,
                extras=sen.extras,
                last_time_used=date.today(),
                type=sen.type,
                origin=WordOrigin.SAVED,
                source_type=SourceTypes.SHORT_VIDEO,
                short_video=video_obj,
                user=user
            ).save()
        # --------------------------VIDEO---------------------------------------------

        # --------------------------CARDS---------------------------------------------
        console.info('Adding cards to user favorites...')
        card_obj = InfoCard.objects.get(id=1)
        sentence_obj = ResourceSentence.objects.filter(info_card=card_obj.id)

        for sen in sentence_obj:
            UserSentence(
                sentence=sen.sentence,
                meaning=sen.meaning,
                extras=sen.extras,
                last_time_used=date.today(),
                type=sen.type,
                origin=WordOrigin.SAVED,
                source_type=SourceTypes.INFO_CARD,
                info_card=card_obj,
                user=user
            ).save()
        # --------------------------CARDS---------------------------------------------

        console.info('Successfully completed!')
