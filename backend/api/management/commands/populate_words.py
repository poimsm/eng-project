from django.core.management.base import BaseCommand
from api.serializers import WordModelSerializer
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Migrate words'

    def handle(self, *args, **kwargs):

        print('--------------------------------')
        print('      POPULATE WORDS            ')
        print('--------------------------------')

        try:
            print('Reading category index...')
            categories = []
            categories_file = open(os.path.join(
                settings.BASE_DIR, 'data/categories/in_use/index.txt'))
            for line in categories_file.readlines():
                cat = line.strip()
                if cat != '':
                    categories.append(cat.lower())
            categories_file.close()

            print('Reading all words per category...')
            words = []
            for cat in categories:
                file = open(os.path.join(settings.BASE_DIR,
                            'data/categories/in_use/' + cat + '.txt'))
                for line in file.readlines():
                    word = line.strip()
                    if word != '':
                        words.append(word.lower())
                file.close()

            print('Migrating all words...')
            for word in set(words):
                word_serializer = WordModelSerializer(data={
                    'word': word
                })

                if(word_serializer.is_valid()):
                    word_serializer.save()

            print('Successfully completed!')

        except Exception as err:
            raise SystemExit(err)
