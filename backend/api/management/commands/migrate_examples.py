import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from api.models import Example, ActivityTypes
from api.helpers import console


def read_JSON_file(path):
    example_file = open(os.path.join(settings.BASE_DIR, path))
    data = example_file.read()
    example_file.close()
    return json.loads(data)


class Command(BaseCommand):
    help = 'Migrate words'

    def handle(self, *args, **kwargs):

        console.info('--------------------------------')
        console.info('     MIGRATE EXAMPLES INIT      ')
        console.info('--------------------------------')

        console.info('Reading index...')
        examples = read_JSON_file('data/examples/index.json')

        AUDIO_URL = settings.SITE_DOMAIN + '/media/audios/'

        console.info('Audio base URL: ' + AUDIO_URL)

        console.info('Migrating ' + str(len(examples)) + ' examples...')
        for ex in examples:
            example_obj = Example(
                id=ex['id'],
                voice_url=AUDIO_URL + ex['voice_file'],
                example=read_JSON_file('data/examples/' + ex['example_file'])
            )

            if ex['type'] == 'question_activity':
                example_obj.type = ActivityTypes.QUESTION
                example_obj.question_id = ex['question_id']
                example_obj.word_id = ex['word_id']
            else:
                example_obj.type = ActivityTypes.DESCRIBE_IMAGE
                example_obj.image_id = ex['image_id']

            example_obj.save()

        console.info('Migration completed successfully')