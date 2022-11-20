# Framework
from django.core.management.base import BaseCommand
from django.conf import settings
import os
from os.path import exists
import traceback

# Custom
from api.models import Difficulty, Question, Word, Style
from api.helpers import console, unique, read_JSON_file


class Command(BaseCommand):
    help = 'Create questions'

    def handle(self, *args, **kwargs):

        console.info('--------------------------------')
        console.info('    POPULATE QUESTIONS          ')
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
            questions = read_JSON_file('data/questions/questions.json')

            AUDIO_URL = settings.SITE_DOMAIN + '/media/question_audios/'
            IMAGE_URL = settings.SITE_DOMAIN + '/media/question_images/'

            console.info('Audio base URL: ' + AUDIO_URL)

            counter = 0
            for q in questions:
                if q['ready'] and q['is_new']:
                    counter += 1

            console.info('Creating ' + str(counter) + ' questions...')

            for q in questions:
                if not (q['ready'] and q['is_new']):
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
                            word_line = line.strip()
                            word = ''
                            meaning = ''
                            is_easy = False
                            if word_line != '':
                                if '[easy]' in word_line:
                                    split = word_line.split('[easy]')
                                    word = split[0]
                                    meaning = split[1]
                                    is_easy = True
                                else:
                                    word = word_line
                                words.append({
                                    'word': word.strip().lower(),
                                    'meaning': meaning.strip(),
                                    'is_easy': is_easy
                                })
                        cat_file.close()
                    else:
                        console.warning('category not found: ' + cat)

                mixed_path = os.path.join(
                    settings.BASE_DIR, 'data/mixed/mixed_' + str(q['id']) + '.txt')

                if exists(mixed_path):
                    mixed_file = open(mixed_path)
                    for line in mixed_file.readlines():
                        word_line = line.strip()
                        word = ''
                        meaning = ''
                        is_easy = False
                        if word_line != '':
                            if '[easy]' in word_line:
                                split = word_line.split('[easy]')
                                word = split[0]
                                meaning = split[1]
                                is_easy = True
                            else:
                                word = word_line
                            words.append({
                                'word': word.strip().lower(),
                                'meaning': meaning.strip(),
                                'is_easy': is_easy
                            })
                    mixed_file.close()
                else:
                    console.warning('File does not exist')

                difficultyDic = {
                    'easy': 0,
                    'moderate': 1,
                    'complex': 2,
                }

                for word in unique(words):
                    try:
                        word_obj = Word.objects.get(word=word['word'])
                    except Word.DoesNotExist:
                        word_obj = Word(
                            word=word['word'],
                            meaning=word['meaning'],
                            difficulty=Difficulty.EASY if word['is_easy'] else Difficulty.UNKNOWN
                        )
                        word_obj.save()

                    try:
                        question_obj = Question.objects.get(id=q['id'])
                    except Question.DoesNotExist:
                        question_obj = Question(
                            id=q['id'],
                            question=q['question'],
                            voice_url=AUDIO_URL + q['voice_file'],
                            image_url=IMAGE_URL + q['image_file'],
                            difficulty=difficultyDic[q['difficulty']],
                            type=q['type']
                        )
                        question_obj.save()

                        Style(
                            background_screen=q['style']['background_screen'],
                            background_challenge=q['style']['background_challenge'],
                            use_gradient=q['style']['use_gradient'],
                            bottom_gradient_color=q['style']['bottom_gradient_color'],
                            top_gradient_color=q['style']['top_gradient_color'],
                            question_position=q['style']['question_position'],
                            image_position=q['style']['image_position'],
                            question_font_size=q['style']['question_font_size'],
                            question_opacity=q['style']['question_opacity'],
                            question=question_obj
                        ).save()

                    question_obj.words.add(word_obj)

            console.info('Successfully completed!')

        except:
            traceback.print_exc()
            console.error('Process Failed!')
