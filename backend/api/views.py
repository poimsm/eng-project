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
    word = 'draw_back'
    synonyms = []
    # for syn in wn.synsets(word, pos=wn.VERB):
    
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

    unique = sorted(set(synonym for synonym in synonyms if synonym != word))
    
    result = ''
    for syn in unique:
        result += syn + '; '

    return HttpResponse(result)

# def hola(request):
#     word = 'deposit'
#     dog = wn.synsets('animal', 'n')[0]
#     paw = wn.synsets('cat', 'n')[0]

#     print(type(dog), type(paw), dog.wup_similarity(paw))
#     a = dog.wup_similarity(paw)

#     return HttpResponse(a)

def hola3(request):
    word = 'deposit'
    dog = wn.synsets('animal', 'n')[0]
    paw = wn.synsets('cat', 'n')[0]

    print(type(dog), type(paw), dog.wup_similarity(paw))
    a = dog.wup_similarity(paw)

    return HttpResponse(a)

    