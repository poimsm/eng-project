from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from users.models import User
from api.models import Word, Question
from api.serializers import UserModelSerializer
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


def hola(request):
    setence="I'm likeee you-to combined hardwork"

    # res = is_common_words('you')

    # literal_question_ids = literal_search(setence)
    # refine_questions = refine_search(setence)

    # aa = get_word_forms('jump')


    # bb = aa['n'] | aa['a'] | aa['v'] | aa['r']
    # jj = {'100', '200', '200'}
    # ee = ['100', '200', '200']
    # print('HOOOLAAAAAAAAAAA')
    # log.info(type(bb))

    # cc = str(type(jj)) + 'hmm'

    # arr = []

    # for b in bb:
    #     arr.append(b + ';')


    words = tokenize_words(str(setence))
    literal_question_ids = literal_search(words)

    setence = TextBlob(setence)
    setence = setence.correct()
    words = tokenize_words(str(setence))
    refined_question_ids = refined_search(words)

    all_ids = set(literal_question_ids + refined_question_ids)

    arr = []
    for b in all_ids:
        arr.append(str(b) + ',')



    # return HttpResponse(len(words))
    # return HttpResponse(list(bb))



    # literal_search
    return HttpResponse(arr)



def tokenize_words(setence):
    words = re.findall(r"\w+", setence.strip())
    words = filter(lambda w: len(w) > 2, words)
    words = filter(lambda w: not w.lower() in common_words_list, words)
    return list(words)

def is_common_words(word):
    if(len(word) <= 2):
        return True

    common = common_words_list
    return word.lower() in common

# def literal_tokenization():
#     pass

# def grammar_checker():
#     pass

# def nltk_tokenization():
#     pass

# def search_phrasal_verbs(word):
#     pass

def literal_search(words):
    question_ids = []
    for word in words:
        try:
            word_obj = Word.objects.get(word=word)
            questions_list = Question.objects.filter(words__id=word_obj.id)
            for q in questions_list:
                question_ids.append(q.id)

        except Word.DoesNotExist:
            print('do nothing')

    return question_ids

def literal_search2(txt):
    words = re.findall(r"\w+", txt)
    words = filter(lambda w: not is_common_words(w), words)

    questions = []
    for word in words:
        try:
            word_obj = Word.objects.get(word=word)
            questions_list = Question.objects.filter(words__id=word_obj.id)
            for q in questions_list:
                questions.append(q.id)

        except Word.DoesNotExist:
            print('do nothing')

    return questions
    

def refined_search(words):
    # pass
    # all_word = []
    all_forms = set()
    for word in words:
        # get_word_forms(word)
        # log.info(word)
        forms = get_word_forms(word)
        all_forms = all_forms | forms['n'] | forms['a'] | forms['v'] | forms['r']
    
    questions_ids = []
    for word in all_forms:
        log.info(word)
        try:
            word_obj = Word.objects.get(word=word)
            questions_list = Question.objects.filter(words__id=word_obj.id)
            for q in questions_list:
                questions_ids.append(q.id)

        except Word.DoesNotExist:
            log.info('No Existe::: ' + word)
            print('do nothing')
    
    return questions_ids
    # get_word_forms("president")
    # text = TextBlob(setence)
    # text = text.correct()
    # word_tokenize(text)


# def word_search():
#     # Buscar todas las formas de las palabras,
#     # conjugaciones, adjetivos, etc
#     pass


# def add_word(request):
#     return HttpResponse('add_word')


    