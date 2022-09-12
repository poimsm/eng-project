from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from users.models import User
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
    return HttpResponse('hooola')

# def is_common_words(word):
#     if(len(word) <= 2):
#         return True

#     common = ['the', 'you', 'the', 'this']
#     return word.lower() in common

# def literal_tokenization():
#     pass

# def grammar_checker():
#     pass

# def nltk_tokenization():
#     pass

# def search_phrasal_verbs(word):
#     pass

# def literal_search(txt):
#     # buscar palabras directamente una a una en DB
#     words = re.findall(r"\w+", txt)
#     for word in words:
#         is_common_words(word)
    
#     pass

# def word_search():
#     # Buscar todas las formas de las palabras,
#     # conjugaciones, adjetivos, etc
#     pass


# def add_word(request):
#     return HttpResponse('add_word')

# def migrate_words(request):
#     return HttpResponse('migrate_words')

# def migrate_questions(request):
#     return HttpResponse('migrate_questions')

    