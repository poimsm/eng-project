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
import logging
log = logging.getLogger('api_v1')
import inflect


 
# Just to make it a bit more readable
WN_NOUN = 'n'
WN_VERB = 'v'
WN_ADJECTIVE = 'a'
WN_ADJECTIVE_SATELLITE = 's'
WN_ADVERB = 'r'

    # """ Transform a verb to the closest noun: die -> death """
    # verb_synsets = wn.synsets(verb_word, pos="v")

    # # Word not found
    # if not verb_synsets:
    #     return []

    # # Get all verb lemmas of the word
    # verb_lemmas = [l for s in verb_synsets \
    #                for l in s.lemmas if s.name.split('.')[1] == 'v']

    # # Get related forms
    # derivationally_related_forms = [(l, l.derivationally_related_forms()) \
    #                                 for l in    verb_lemmas]

    # # filter only the nouns
    # related_noun_lemmas = [l for drf in derivationally_related_forms \
    #                        for l in drf[1] if l.synset.name.split('.')[1] == 'n']

    # # Extract the words from the lemmas
    # words = [l.name for l in related_noun_lemmas]
    # len_words = len(words)

    # # Build the result in the form of a list containing tuples (word, probability)
    # result = [(w, float(words.count(w))/len_words) for w in set(words)]
    # result.sort(key=lambda w: -w[1])

    # # return all the possibilities sorted by probability
    # return result
 
def convert(word, from_pos, to_pos):
    """ Transform words given from/to POS tags """

    synsets = wn.synsets(word, pos=from_pos)

    # Word not found
    if not synsets:
        return []

    # Get all lemmas of the word (consider 'a'and 's' equivalent)
    lemmas = []
    for s in synsets:
        for l in s.lemmas():
            if s.name().split('.')[1] == from_pos or from_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and s.name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                lemmas += [l]

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]

    # filter only the desired pos (consider 'a' and 's' equivalent)
    related_noun_lemmas = []

    for drf in derivationally_related_forms:
        for l in drf[1]:
            if l.synset().name().split('.')[1] == to_pos or to_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and l.synset().name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                related_noun_lemmas += [l]

    # Extract the words from the lemmas
    words = [l.name() for l in related_noun_lemmas]
    len_words = len(words)

    # Build the result in the form of a list containing tuples (word, probability)
    result = [(w, float(words.count(w)) / len_words) for w in set(words)]
    result.sort(key=lambda w:-w[1])

    # return all the possibilities sorted by probability
    return result


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
def hola7(request):
    pass
    # UNCONDITIONALLY FORM THE PLURAL
    # p = inflect.engine()

    # word="dog"
    # cat_count=3


    # log.debug("The plural of ", word, " is ", p.plural(word))


    # # CONDITIONALLY FORM THE PLURAL

    # log.debug("I saw", cat_count, p.plural("cat", cat_count))


    # # FORM PLURALS FOR SPECIFIC PARTS OF SPEECH

    # log.debug(
    #     p.plural_noun("I", N1),
    #     p.plural_verb("saw", N1),
    #     p.plural_adj("my", N2),
    #     p.plural_noun("saw", N2),
    # )

def hola8(request):
    log.debug("hypernym")
    aa = wn.synset('bank.n.01').hypernyms()
    log.debug(aa)
    log.debug("Hypernym for 'cat': ", wn.synset('cat.n.01').hypernyms())
    return HttpResponse("hmmm")


def hola(request):
    log.debug('akii vaaaaa 0')

    # WN_NOUN = 'n'
    # WN_VERB = 'v'
    # WN_ADJECTIVE = 'a'
    # WN_ADJECTIVE_SATELLITE = 's'
    # WN_ADVERB = 'r'
    
    log.debug('akii vaaaaa 4')
    log.debug(convert("tire", WN_VERB, WN_ADJECTIVE))
    log.debug(get_word_forms("tiredness"))
    

    return HttpResponse('nadaaaa')

def hola10(request):
    word = 'deposit'
    synonyms = []
    # for syn in wn.synsets(word, pos=wn.VERB):
    
    for syn in wn.synsets(word, pos=wn.VERB):
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

    