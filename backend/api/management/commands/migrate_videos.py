from django.core.management.base import BaseCommand
from api.models import ShortVideo, Sentence, SourceTypes, Collocation

from django.conf import settings
import os
import json
import traceback
from api.helpers import console


class Command(BaseCommand):
    help = 'Migrate short videos'

    def handle(self, *args, **kwargs):

        console.info('--------------------------------')
        console.info('    MIGRATE VIDEOS INIT          ')
        console.info('--------------------------------')

        try:

            console.info('Reading videos JSON file...')
            jsonFile = open(os.path.join(
                settings.BASE_DIR, 'data/videos/videos.json'))

            videos = json.load(jsonFile)
            jsonFile.close()

            MEDIA_URL = settings.SITE_DOMAIN + '/media/videos/'
            IMAGE_URL = settings.SITE_DOMAIN + '/media/card_images/'

            console.info('Audio base URL: ' + MEDIA_URL)
            console.info('Migrating ' + str(len(videos)) + ' videos...')

            for video in videos:
                video_obj = ShortVideo(
                    id=video['id'],
                    cover=IMAGE_URL + video['cover'],
                    url=MEDIA_URL + video['video_file']
                )

                video_obj.save()

                for sen in video['sentences']:
                    Sentence(
                        sentence=sen['sentence'],
                        meaning=sen['meaning'],
                        extras=sen['extras'],
                        type=sen['type'],
                        source_type=SourceTypes.SHORT_VIDEO,
                        short_video=video_obj
                    ).save()

                for coll in video['collocations']:
                    Collocation(
                        text=coll,
                        source_type=SourceTypes.INFO_CARD,
                        info_card=video_obj
                    ).save()

            console.info('Migration completed successfully')

        except:
            traceback.print_exc()
