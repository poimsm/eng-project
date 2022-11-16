import json
import os
import traceback
from django.conf import settings
from django.core.management.base import BaseCommand
from api.models import Example, Question
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
        console.info('     POPULATE EXAMPLES          ')
        console.info('--------------------------------')

        try:
            console.info('Reading index...')
            examples = read_JSON_file('data/examples/index.json')

            AUDIO_URL = settings.SITE_DOMAIN + '/media/audios/'

            console.info('Audio base URL: ' + AUDIO_URL)

            counter = 0
            for ex in examples:
                if ex['is_new']: counter += 1

            console.info('Creating ' + str(counter) + ' examples...')

            for ex in examples:
                if not ex['is_new']: continue
                Example.objects.update_or_create(
                    id=ex['id'],
                    defaults={
                        'id': ex['id'],
                        'voice_url': AUDIO_URL + ex['voice_file'],
                        'example': read_JSON_file(
                            'data/examples/' + ex['example_file']),
                        'question': Question.objects.get(id=ex['question_id']),
                        'word_text': ex['word_text']
                    }
                )

            console.info('Successfully completed!')
        except:
            traceback.print_exc()
            console.error('Process Failed!')
