import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from api.models import ActivityTypes, DescribeImageActivity, Style
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
        console.info('     MIGRATE IMAGES INIT        ')
        console.info('--------------------------------')

        console.info('Reading index...')
        images = read_JSON_file('data/images/index.json')

        IMAGE_URL = settings.SITE_DOMAIN + '/media/images/'

        console.info('Image base URL: ' + IMAGE_URL)

        console.info('Migrating ' + str(len(images)) + ' images...')
        for img in images:
            DescribeImageActivity(
                id=img['id'],
                image_url=IMAGE_URL + img['image_file']
            ).save()

            Style(
                background_screen=img['style']['background_screen'],
                activity_id=img['id'],
                type=ActivityTypes.DESCRIBE_IMAGE
            ).save()

        console.info('Migration completed successfully')
