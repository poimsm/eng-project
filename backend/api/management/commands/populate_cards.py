from django.core.management.base import BaseCommand
from api.models import InfoCard, ResourceSentence, SourceTypes, Collocation

from django.conf import settings
import os
import json
import traceback
from api.helpers import console


class Command(BaseCommand):
    help = 'Migrate info cards'

    def handle(self, *args, **kwargs):

        console.info('--------------------------------')
        console.info('    POPULATE CARDS              ')
        console.info('--------------------------------')

        try:

            console.info('Reading cards JSON file...')
            jsonFile = open(os.path.join(
                settings.BASE_DIR, 'data/cards/cards.json'))

            cards = json.load(jsonFile)
            jsonFile.close()

            AUDIO_URL = settings.SITE_DOMAIN + '/media/card_audios/'
            IMAGE_URL = settings.SITE_DOMAIN + '/media/card_images/'

            console.info('Audio base URL: ' + AUDIO_URL)

            counter = 0
            for ex in cards:
                if ex['is_new']: counter += 1

            console.info('Creating ' + str(counter) + ' cards...')
            

            for card in cards:
                if not ex['is_new']: continue
                
                card_obj = InfoCard(
                    id=card['id'],
                    image_url=IMAGE_URL + card['image_file'],
                    voice_url=AUDIO_URL + card['audio_file']
                )

                card_obj.save()

                for sen in card['sentences']:
                    ResourceSentence(
                        sentence=sen['sentence'],
                        meaning=sen['meaning'],
                        extras=sen['extras'],
                        type=sen['type'],
                        source_type=SourceTypes.INFO_CARD,
                        info_card=card_obj
                    ).save()

                for coll in card['collocations']:
                    Collocation(
                        text=coll,
                        source_type=SourceTypes.INFO_CARD,
                        info_card=card_obj
                    ).save()

            console.info('Successfully completed!')

        except:
            traceback.print_exc()
            console.error('Process Failed!')
