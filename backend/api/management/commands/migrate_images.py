import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from api.models import DescribeImageActivity
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
        images = read_JSON_file('data/images/index.json')

        IMAGE_URL = settings.SITE_DOMAIN + '/media/images/'

        console.info('Audio base URL: ' + IMAGE_URL)

        console.info('Migrating ' + str(len(images)) + ' images...')
        for img in images:
            img_obj = DescribeImageActivity(
                id=img['id'],
                image_url=IMAGE_URL + img['image_file']
            )

            img_obj.save()

        console.info('Migration completed successfully')
