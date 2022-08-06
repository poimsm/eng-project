from django.shortcuts import render
from django.http import HttpResponse
from textblob import TextBlob

import time

import nltk
# from nltk.corpus import wordnet
# from nltk.stem import wordnet
from nltk.corpus import wordnet as wn
# from nltk.stem.wordnet import WordNetLemmatiz

words = [
    'jump',
    'run',
    'read',
    'swim',
    'row'
]

def get_synonyms(word, pos):
    for synset in wn.synsets(word, pos=pos_to_wordnet_pos(pos)):
        for lemma in synset.lemmas():
            yield lemma.name()

def pos_to_wordnet_pos(penntag, returnNone=False):
#    ' Mapping from POS tag word wordnet pos tag '
    morphy_tag = {'NN':wn.NOUN, 'JJ':wn.ADJ,
                  'VB':wn.VERB, 'RB':wn.ADV}
    try:
        return morphy_tag[penntag[:2]]
    except:
        return None if returnNone else ''



def extract_words(sentence):
    blob = TextBlob(sentence)
    text_lower = blob.lower()    
    text_corrected = text_lower.correct()
    text = TextBlob(str(text_corrected))
    return text.words

def get_meaning(sentence):
    blob = TextBlob(sentence)
    text_lower = blob.lower()    
    text_corrected = text_lower.correct()
    text = TextBlob(str(text_corrected))
    return text.words

def check_words(sentence):
    blob = TextBlob(sentence)
    text_lower = blob.lower()    
    text_corrected = text_lower.correct()
    text = TextBlob(str(text_corrected))
    return text.words

def get_tag(tag):
    morphy_tag = {
        'NN': wn.NOUN,
        'JJ': wn.ADJ,
        'VB': wn.VERB,
        'RB': wn.ADV,
        'VB': wn.VERB,
        'VB': wn.VERB,
        'VB': wn.VERB,
        'VB': wn.VERB,
        'VB': wn.VERB,
    }

    if tag in morphy_tag:
        return morphy_tag[tag]
    else:
        return '';
    

def get_tag2(tag):
    morphy_tag = {
        'NN': 'wn.NOUN',
        'JJ': 'wn.ADJ',
        'VB': 'wn.VERB',
        'RB': 'wn.ADV'
    }
    return morphy_tag[tag]

def check_verb(verb):
    word = nltk.stem.WordNetLemmatizer().lemmatize(verb, wn.VERB)
    synonyms = []
    for syn in wn.synsets(word, pos=wn.VERB):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

    unique = sorted(set(synonym for synonym in synonyms if synonym != word))
    return unique

def hola(request):
    synonyms = []
    for syn in wn.synsets('desks', pos=wn.NOUN):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

    unique = sorted(set(synonym for synonym in synonyms if synonym != 'take'))
    
    result = ''
    for syn in unique:
        result += syn + '; '

    return HttpResponse(result)

def hola6(request):
    user_input = 'Get drawn byy'
    # match_question()

    return HttpResponse(result)

def hola5(request):
    text = nltk.word_tokenize("all")
    # word = 'I like jumping'
    word, tag = zip(*nltk.pos_tag(text))

    return HttpResponse(tag[0])


def hola4(request):
    text = nltk.word_tokenize("I refuse to jump")
    word = 'jumping'
    word = nltk.stem.WordNetLemmatizer().lemmatize(word, wn.VERB)
    synonyms = []
    for syn in wn.synsets('jump', pos=wn.VERB):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

    unique = sorted(set(synonym for synonym in synonyms if synonym != 'jump'))
    
    result = ''
    for syn in unique:
        result += syn + '; '

    return HttpResponse(result)

def hola3(request):
    text = nltk.word_tokenize("I refuse to jump")

    for word, tag in nltk.pos_tag(text):
        print(f'word is {word}, POS is {tag}')

    unique = sorted(set(synonym for synonym in get_synonyms(word, tag) if synonym != word))

    result = ''
    for synonym in unique:
        result += synonym + '; '

    return HttpResponse(result)


def hola2(request):
    # word = request.GET['var']
    # syn = wordnet.synsets(word)
    # aa = syn[0].definition()

    # aa = nltk.__version__

    user_input = 'Get drawn byy'
    extract_words(user_input)

    

    result3 = 'NADA'

    # for c in cc:
    #     result3 += str(c) + '; '

    # result2 = str(sentence.correct())

    synonyms = []
    for syn in wordnet.synsets('help'):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

    aa = ''
    for syn in synonyms:
        aa += syn + '; '


    return HttpResponse(result3)
    # return HttpResponse('hoolaaa 11')

