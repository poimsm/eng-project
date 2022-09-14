from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

from users.models import User
from api.models import Word, Question, ImageActivity
from api.serializers import (
    QuestionModelSerializer,
    UserModelSerializer,
    ImageActivityModelSerializer
)
from users.serializers import CustomTokenObtainPairSerializer
import uuid
from textblob import TextBlob
import nltk
from nltk.corpus import wordnet as wn
from django.http import HttpResponse
from word_forms.word_forms import get_word_forms
import re
import logging
log = logging.getLogger('api_v1')
from api.data.common_words import common_words_list
from nltk.tokenize import word_tokenize
from random import sample, shuffle


@api_view(['POST'])
def create_user(request):
    uid = uuid.uuid4()
    random_user = uid.hex
    data = {
        'username': 'random_user',
        'email':  random_user + '@fake.com',
        'password': random_user
    }
    serializer = UserModelSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

        class UserPayload:
            id = serializer.data['id']

        refresh = CustomTokenObtainPairSerializer().get_token(UserPayload)

        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def combine_unique(list1, list2):    
    list = list1 + list2

    memory = []
    unique = []

    for item in list:
        if item['id'] not in memory:
            memory.append(item['id'])
            unique.append(item)

    return unique

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def hola(request):
    setence="I'm likeee you-to combined hardwork"

    # question_obj = Question.objects.get(id=12)
    # serializer = QuestionModelSerializer(question_obj)
    # return Response(serializer.data, status=status.HTTP_201_CREATED)


    # images = ImageActivity.objects.all()
    # aa = ImageActivityModelSerializer(images, many=True)
    # log.info(aa.data)

    # return Response(aa.data, status=status.HTTP_200_OK)
    
    
    words = tokenize_words(str(setence))
    literal_question = literal_search(words)

    setence = TextBlob(setence)
    setence = setence.correct()
    words = tokenize_words(str(setence))
    refined_question = refined_search(words)

    found_questions = combine_unique(literal_question, refined_question)
    activities = create_activity_package(found_questions)

    shuffle(activities)
    shuffle(activities)
    shuffle(activities)

    return Response(activities, status=status.HTTP_200_OK)


def create_activity_package(found_questions):

    activities = []

    if len(found_questions) < 5:
        questions = Question.objects.exclude(id__in=ids)
        questions_serializer = QuestionModelSerializer(questions, many=True)

        images = ImageActivity.objects.all()
        images_serializer = ImageActivityModelSerializer(images, many=True)

        total = 15 - len(found_questions)

        sample_questions = sample(questions_serializer.data, round(total/2))
        sample_imgs = sample(images_serializer.data, round(total/2))

        for img in sample_imgs:
            activities.append({
                'id': img['id'],
                'image': img,
                'type': 'image_activity',
                'word': None
            })

        for q in sample_questions:
            activities.append({
                'id': q['id'],
                'question': q,
                'type': 'question',
                'word': None
            })
    else:        
        sample_found_questions = sample(found_questions, 5)
        ids = [q['id'] for q in sample_found_questions]

        questions = Question.objects.exclude(id__in=ids)
        questions_serializer = QuestionModelSerializer(questions, many=True)

        images = ImageActivity.objects.all()
        images_serializer = ImageActivityModelSerializer(images, many=True)
        
        sample_questions = sample(questions_serializer.data, 5)        
        sample_imgs = sample(images_serializer.data, 5)

        for q in sample_questions:
            activities.append({
                'id': q['id'],
                'question': q,
                'type': 'question',
                'word': None
            })

        for img in sample_imgs:
            activities.append({
                'id': img['id'],
                'image': img,
                'type': 'image_activity',
                'word': None
            })

    activities += found_questions
    return activities
    # Products.objects.filter(id__in=ids)
        



def tokenize_words(setence):
    words = re.findall(r"\w+", setence.strip())
    words = filter(lambda w: len(w) > 2, words)
    words = filter(lambda w: not w.lower() in common_words_list, words)
    return list(words)



# def search_phrasal_verbs(word):
#     pass



def literal_search(words):
    questions = []
    for word in words:
        try:
            word_obj = Word.objects.get(word=word)
            questions_list = Question.objects.filter(words__id=word_obj.id)
            for q in questions_list:
                questions.append({
                    'id': q.id,
                    'question': QuestionModelSerializer(q).data,
                    'type': 'question',
                    'word': word_obj.word
                })

        except Word.DoesNotExist:
            print('do nothing')

    return questions


def refined_search(words):
    all_forms = set()
    for word in words:
        forms = get_word_forms(word)
        all_forms = all_forms | forms['n'] | forms['a'] | forms['v'] | forms['r']
    
    questions = []
    for word in all_forms:
        try:
            word_obj = Word.objects.get(word=word)
            questions_list = Question.objects.filter(words__id=word_obj.id)
            for q in questions_list:
                questions.append({
                    'id': q.id,
                    'question': QuestionModelSerializer(q).data,
                    'type': 'question',
                    'word': word_obj.word
                })

        except Word.DoesNotExist:
            print('do nothing')
    
    return questions



# def add_word(request):
#     return HttpResponse('add_word')


    