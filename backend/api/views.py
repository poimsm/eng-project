from random import sample, shuffle
from nltk.tokenize import word_tokenize

# Data
from api.data.common_words import common_words_list
from api.data.phrasal_verbs import phrasal_verbs
from api.data.slangs import slangs

from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import (
    api_view, renderer_classes, permission_classes
)

from django.contrib.auth.hashers import make_password
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse


from users.models import User
from api.models import Word, QuestionActivity, DescribeImageActivity
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

from nltk.stem.wordnet import WordNetLemmatizer

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def create_fake_user(request):
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


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([permissions.IsAuthenticated])
def user_data(request):
    user_id = request.GET.get('id', False)
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            serializer = UserModelSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            Response({}, status=status.HTTP_404_NOT_FOUND)

    return Response({}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([permissions.IsAuthenticated])
def user_register(request):
    try:
        data = request.data.copy()
        user = User.objects.get(id=request.user.id)
        user.verified = True
        user.password = make_password(
            data['password'], salt=None, hasher='default')
        user.email = data['email']
        user.save()

        user_data = UserModelSerializer(user).data
        del user_data['password']

        return Response(user_data, status=status.HTTP_201_CREATED)
    except:
        Response({}, status=status.HTTP_400_BAD_REQUEST)


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
# @permission_classes([permissions.IsAuthenticated])
def get_post(request):
    return Response({'msg': 'todo funcionando x3'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def hola(request):
    # sentence='go up';
    # sentence='went out';
    # sentence='I hang you out';
    # sentence='hold on!';
    # sentence='hold me on!';
    # sentence='I hold realy you do me on!';
    # sentence='OK! I catch you up later!!';
    # sentence='I want to broken up!';
    # sentence='I gave up, I want to broken up!';
    sentence = 'I will motherfucker you!'
    phrasal_verbs = extract_phrasal_verbs(sentence)

    hasSlang = check_for_slangs(sentence)
    return Response({'len': hasSlang}, status=status.HTTP_200_OK)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def hola3(request):
    sentence = "I'm likeee you-to combined hardwork"

    # question_obj = QuestionActivity.objects.get(id=12)
    # serializer = QuestionModelSerializer(question_obj)
    # return Response(serializer.data, status=status.HTTP_201_CREATED)

    # images = DescribeImageActivity.objects.all()
    # aa = ImageActivityModelSerializer(images, many=True)
    # log.info(aa.data)

    # return Response(aa.data, status=status.HTTP_200_OK)

    hasSlang = check_for_slangs(sentence)
    if hasSlang:
        return Response({'message': 'Offensive statement'}, status=status.HTTP_400_BAD_REQUEST)        

    words = tokenize_words(str(sentence))
    literal_questions = literal_search(words)

    sentence_blob = TextBlob(sentence)
    sentence_blob = sentence.correct()
    words = tokenize_words(str(sentence_blob))
    refined_questions = refined_search(words)

    phrasal_verbs = extract_phrasal_verbs(sentence)
    phrasal_verbs_questions = literal_search(phrasal_verbs)

    found_questions = combine_unique(literal_questions, refined_questions, phrasal_verbs_questions)
    activities = create_activity_package(found_questions)    

    shuffle(activities)
    shuffle(activities)
    shuffle(activities)

    return Response(activities, status=status.HTTP_200_OK)


def create_activity_package(found_questions):

    activities = []

    if len(found_questions) < 5:
        questions = QuestionActivity.objects.exclude(id__in=ids)
        questions_serializer = QuestionModelSerializer(questions, many=True)

        images = DescribeImageActivity.objects.all()
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

        questions = QuestionActivity.objects.exclude(id__in=ids)
        questions_serializer = QuestionModelSerializer(questions, many=True)

        images = DescribeImageActivity.objects.all()
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

def extract_phrasal_verbs(sentence):
    words_raw = re.findall(r"\w+", sentence.strip())

    words = []
    for w in words_raw:
        words.append(WordNetLemmatizer().lemmatize(w,'v'))        

    possible_match = []
    for v in phrasal_verbs:
        verb = v.split('_')[0]
        for word in words:
            if word == verb:
                if word not in possible_match:
                    possible_match.append({
                        'word': word,
                        'phrasal_verb': v,
                        'end': v.split('_')[1]
                    })

    matches = []
    for m in possible_match:
        for w in words:
            if w == m['end']:
                if m['phrasal_verb'] not in matches:
                    matches.append(m['phrasal_verb'])
    return matches

def check_for_slangs(sentence):
    words = re.findall(r"\w+", sentence.strip())
    words = filter(lambda w: w.lower() in slangs, words)
    return len(list(words)) != 0


def tokenize_words(sentence):
    words = re.findall(r"\w+", sentence.strip())
    words = filter(lambda w: len(w) > 2, words)
    words = filter(lambda w: not w.lower() in common_words_list, words)
    return list(words)


def literal_search(words):
    questions = []
    for word in words:
        try:
            word_obj = Word.objects.get(word=word)
            questions_list = QuestionActivity.objects.filter(words__id=word_obj.id)
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
            questions_list = QuestionActivity.objects.filter(words__id=word_obj.id)
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
