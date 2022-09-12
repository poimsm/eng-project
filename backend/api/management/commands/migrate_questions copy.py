from django.core.management.base import BaseCommand
from api.serializers import WordModelSerializer, QuestionModelSerializer
from api.models import Word, Question

from django.conf import settings
import os
import json
from os.path import exists
import traceback


class Command(BaseCommand):
    help = 'Migrate questions'

    def handle(self, *args, **kwargs):

        print('--------------------------------')
        print('    MIGRATE QUESTIONS INIT      ')
        print('--------------------------------')

        try:

            print('hooola')
            # wordModel = Word.objects.get(word='adasd').exist()
            # print(wordModel)

            # try:
            #     wordModel = Word.objects.get(word='hey')
            # except Word.DoesNotExist:
            #     wordModel = None

            # w = Word(word='hmm')
            # w.save()
            # print(w.id, 'idddd')

            # word_serializer = WordModelSerializer(data={
            #                 'word': 'hmm3'
            #             })
            # word_serializer.is_valid()
            # rr = word_serializer.save()
            # print(word_serializer.data['id'], 'iddrr')
        
            # return

            print('Reading category index...')
            index = []
            index_file = open(os.path.join(
                settings.BASE_DIR, 'data/categories/in_use/index.txt'))
            for line in index_file.readlines():
                index.append(line.strip().lower())
            index_file.close()

            print('Reading questions JSON file...')
            jsonFile = open(os.path.join(
                settings.BASE_DIR, 'data/questions/questions.json'))

            questions = json.load(jsonFile)
            jsonFile.close()

            print('Migrating questions...')
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
                        print('WARNING: category not found:', cat)
                
                mixed_path = os.path.join(settings.BASE_DIR, 'data/mixed/mixed_' + str(q['id']) + '.txt')
                print('mixed_path', mixed_path)
                if exists(mixed_path):
                    mixed_file = open(mixed_path)
                    for line in mixed_file.readlines():
                        word = line.strip()
                        if word != '':
                            words.append(word.lower())
                    mixed_file.close()
                else:
                    print('file no existe')
                    

                difficultyDic = {
                    'easy': 0,
                    'moderate': 1,
                    'complex': 2,
                }

                for word in set(words):
                    # wordModel = Word.objects.get(word=word)
                    try:
                        wordModel = Word.objects.get(word=word)
                    except Word.DoesNotExist:
                        wordModel = None

                    if not wordModel:
                        word_obj = Word(word=word)
                        word_obj.save()
                        word_id = word_obj.id
                    else:
                        word_id = wordModel.id


                        # if word_serializer.is_valid():
                        #      = word_serializer.save()
                        # id = device.id



                    question_obj = Question(
                        id=q['id'],
                        difficulty=difficultyDic[q['difficulty']],
                        question=q['question'],
                    )

                    question_obj.words.add(word)

                    question_obj.save()
                    a1.publications.add(p1)
    

                    # question_obj = Question(
                    #     id=q['id'],
                    #     difficulty=difficultyDic[q['difficulty']],
                    #     question=q['question'],
                    #     word=id
                    # )
                    # question_obj.save()


                    # question_serializer = QuestionModelSerializer(data={
                    #     'id': q['id'],
                    #     'difficulty': difficultyDic[q['difficulty']],
                    #     'question': q['question'],
                    #     'word': word_id
                    # })

                    # if(question_serializer.is_valid()):
                    #     question_serializer.save()

            print('Process completed')

        except:
            traceback.print_exc()
