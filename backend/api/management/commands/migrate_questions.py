from django.core.management.base import BaseCommand
from api.models import ActivityTypes, QuestionActivity, Word, QuestionActivity, Style

from django.conf import settings
import os
import json
from os.path import exists
import traceback
from api.helpers import console


class Command(BaseCommand):
    help = 'Migrate questions'

    def handle(self, *args, **kwargs):

        console.info('--------------------------------')
        console.info('    MIGRATE QUESTIONS INIT      ')
        console.info('--------------------------------')

        try:

            console.info('Reading category index...')
            index = []
            index_file = open(os.path.join(
                settings.BASE_DIR, 'data/categories/in_use/index.txt'))
            for line in index_file.readlines():
                index.append(line.strip().lower())
            index_file.close()

            console.info('Reading questions JSON file...')
            jsonFile = open(os.path.join(
                settings.BASE_DIR, 'data/questions/questions.json'))

            questions = json.load(jsonFile)
            jsonFile.close()

            AUDIO_URL = settings.SITE_DOMAIN + '/media/audios/'

            console.info('Audio base URL: ' + AUDIO_URL)
            console.info('Migrating ' + str(len(questions)) + ' questions...')

            for q in questions:
                if not q['ready']:
                    continue

                categories = []
                for cat in q['categories']:
                    categories.append(cat.strip().lower())

                words = []
                for cat in set(categories):
                    if cat in index:
                        cat_file = open(os.path.join(settings.BASE_DIR,
                                                     'data/categories/in_use/' + cat + '.txt'))
                        for line in cat_file.readlines():
                            word = line.strip()
                            if word != '':
                                words.append(word.lower())
                        cat_file.close()
                    else:
                        console.warning('category not found: ' + cat)

                mixed_path = os.path.join(
                    settings.BASE_DIR, 'data/mixed/mixed_' + str(q['id']) + '.txt')

                if exists(mixed_path):
                    mixed_file = open(mixed_path)
                    for line in mixed_file.readlines():
                        word = line.strip()
                        if word != '':
                            words.append(word.lower())
                    mixed_file.close()
                else:
                    console.warning('File does not exist')

                difficultyDic = {
                    'easy': 0,
                    'moderate': 1,
                    'complex': 2,
                }

                for word in set(words):
                    try:
                        word_obj = Word.objects.get(word=word)
                    except Word.DoesNotExist:
                        word_obj = Word(word=word)
                        word_obj.save()

                    try:
                        question_obj = QuestionActivity.objects.get(id=q['id'])
                    except QuestionActivity.DoesNotExist:
                        question_obj = QuestionActivity(
                            id=q['id'],
                            question=q['question'],
                            voice_url=AUDIO_URL + q['voice_file'],
                            image_url=q['image_file'],
                            difficulty=difficultyDic[q['difficulty']]
                        )
                        question_obj.save()

                        Style(
                            background_screen=q['style']['background_screen'],
                            background_word=q['style']['background_word'],
                            activity_id=q['id'],
                            type=ActivityTypes.QUESTION
                        ).save()

                    question_obj.words.add(word_obj)

            console.info('Migration completed successfully')

        except:
            traceback.print_exc()
