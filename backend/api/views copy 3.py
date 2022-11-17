# Python
import math
import re
import copy
import random

# Framework
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import (
    api_view, renderer_classes, permission_classes
)
from django.contrib.auth.hashers import make_password
from rest_framework.renderers import JSONRenderer


# Data
from api.data.common_words import common_words_list
from api.data.phrasal_verbs import phrasal_verbs
from api.data.slangs import slangs
from api.data.expresions import expresions


# Models & serializers
from users.models import User
from api.models import (
    ActivityTypes, Word, Question,
    UserSentence, Example, Style, ShortVideo,
    InfoCard, FavoriteResource, SourceTypes,
    WordTypes, WordOrigin, ResourceSentence,
    Status, Difficulty
)
from api.serializers import (
    QuestionModelSerializer,
    UserModelSerializer,
    UserSentenceModelSerializer,
    ExampleModelSerializer,
    StyleModelSerializer,
    WordModelSerializer,
    ShortVideoModelSerializer,
    InfoCardModelSerializer,
    FavoriteResourceModelSerializer,
    QuestionFullSerializer
)
from users.serializers import CustomTokenObtainPairSerializer

# Libraries
import uuid
from textblob import TextBlob
import nltk
from nltk.corpus import wordnet as wn
from word_forms.word_forms import get_word_forms
import logging
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer


log = logging.getLogger('api_v1')
test_user_id = 1


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


@api_view(['GET'])
@renderer_classes([JSONRenderer])
# @permission_classes([permissions.IsAuthenticated])
def get_post(request):
    return Response({'msg': 'todo funcionando x3'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def hola(request):
    data = get_random_questions([12], 3)
    return Response(data, status=status.HTTP_200_OK)
    # sentence='go up';
    # sentence='went out';
    # sentence='I hang you out';
    # sentence='hold on!';
    # sentence='hold me on!';
    # sentence='I hold realy you do me on!';
    # sentence='OK! I catch you up later!!';
    # sentence='I want to broken up!';
    # sentence='I gave up, I want to broken up!';

    # sentence = 'I will motherfucker you!'
    # phrasal_verbs = extract_phrasal_verbs(sentence)

    # hasSlang = check_for_slangs(sentence)
    # return Response({'len': hasSlang}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
@renderer_classes([JSONRenderer])
def short_video(request):
    if request.method == 'GET':
        videos = ShortVideo.objects.all().order_by('-created')
        user_videos = FavoriteResource.objects.filter(
            source_type=SourceTypes.SHORT_VIDEO,
            user=1,
            status=Status.ACTIVE,
        )

        video_serializer = ShortVideoModelSerializer(videos, many=True)
        video_data = video_serializer.data

        result = []
        for video in video_data:
            is_favorite = False
            for user_vid in user_videos:
                if video['id'] == user_vid.short_video.id:
                    is_favorite = True
            video['is_favorite'] = is_favorite
            result.append(video)

        return Response(result, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data.copy()

        resource_data = {
            'user': 1,
            'short_video': data['video_id'],
            'source_type': SourceTypes.SHORT_VIDEO,
        }

        resource_serializer = FavoriteResourceModelSerializer(
            data=resource_data)
        if resource_serializer.is_valid(raise_exception=True):
            resource_serializer.save()

            sentences = ResourceSentence.objects.filter(
                short_video=data['video_id'],
                status=Status.ACTIVE
            )

            for sen in sentences:
                sen_data = {
                    'sentence': sen.sentence,
                    'meaning': sen.meaning,
                    'extras': sen.extras,
                    'type': sen.type,
                    'origin': WordOrigin.SAVED,
                    'short_video': data['video_id'],
                    'source_type': SourceTypes.SHORT_VIDEO,
                    'user': 1,
                }

                user_sen_serializer = UserSentenceModelSerializer(
                    data=sen_data)

                if user_sen_serializer.is_valid(raise_exception=True):
                    user_sen_serializer.save()

            return Response(resource_serializer.data, status=status.HTTP_201_CREATED)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        data = request.data.copy()
        FavoriteResource.objects.filter(
            user=1,
            short_video=data['video_id']
        ).update(status=Status.DELETED)

        UserSentence.objects.filter(
            user=1,
            short_video=data['video_id'],
        ).update(status=Status.DELETED)
        return Response({}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
@renderer_classes([JSONRenderer])
def info_card(request):
    if request.method == 'GET':
        cards = InfoCard.objects.all().order_by('-created')
        user_cards = FavoriteResource.objects.filter(
            source_type=SourceTypes.INFO_CARD,
            user=1,
            status=Status.ACTIVE
        )

        card_serializer = InfoCardModelSerializer(cards, many=True)
        cards_data = random.sample(card_serializer.data, 2)

        result = []
        for card in cards_data:
            is_favorite = False
            for user_card in user_cards:
                if card['id'] == user_card.info_card.id:
                    is_favorite = True
            card['is_favorite'] = is_favorite
            result.append(card)

        return Response(result, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data.copy()

        resource_data = {
            'user': 1,
            'info_card': data['card_id'],
            'source_type': SourceTypes.INFO_CARD,
        }

        resource_serializer = FavoriteResourceModelSerializer(
            data=resource_data)
        if resource_serializer.is_valid(raise_exception=True):
            resource_serializer.save()

            sentences = ResourceSentence.objects.filter(
                info_card=data['card_id'],
                status=Status.ACTIVE
            )

            for sen in sentences:
                sen_data = {
                    'sentence': sen.sentence,
                    'meaning': sen.meaning,
                    'extras': sen.extras,
                    'type': sen.type,
                    'origin': WordOrigin.SAVED,
                    'info_card': data['card_id'],
                    'source_type': SourceTypes.INFO_CARD,
                    'user': 1,
                }

                user_sen_serializer = UserSentenceModelSerializer(
                    data=sen_data)

                if user_sen_serializer.is_valid(raise_exception=True):
                    user_sen_serializer.save()

            return Response(resource_serializer.data, status=status.HTTP_201_CREATED)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        data = request.data.copy()
        FavoriteResource.objects.filter(
            user=1,
            info_card=data['card_id']
        ).update(status=Status.DELETED)

        UserSentence.objects.filter(
            user=1,
            info_card=data['card_id']
        ).update(status=Status.DELETED)
        return Response({}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@renderer_classes([JSONRenderer])
def user_sentences(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        per_page = 20

        sentences = UserSentence.objects.filter(
            user__id=test_user_id,
            status=Status.ACTIVE
        ).order_by('-created')

        total = sentences.count()
        start = (page - 1)*per_page
        end = page*per_page

        serializer = UserSentenceModelSerializer(
            sentences[start:end], many=True)

        return Response({
            'data': serializer.data,
            'total_items': total,
            'current_page': page,
            'total_pages': math.ceil(total / per_page)
        }, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = 1

        if check_for_slangs(data['sentence']):
            return Response({'message': 'Offensive statement'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSentenceModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        try:
            data = request.data.copy()

            if check_for_slangs(data['sentence']):
                return Response({'message': 'Offensive statement'}, status=status.HTTP_400_BAD_REQUEST)

            sentence = UserSentence.objects.get(id=data['id'])
            serializer = UserSentenceModelSerializer(
                sentence, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        except UserSentence.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            data = request.data.copy()
            UserSentence.objects.update_or_create(id=data['id'], defaults={
                'status': Status.DELETED
            })
            return Response({}, status=status.HTTP_200_OK)
        except UserSentence.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def daily_activities(request):

    sentences = get_sentences(test_user_id)
    questions = get_questions_per_sentence(sentences)

    activities = create_activity_package(questions)
    random.shuffle(activities)

    activities = add_examples(activities)
    activities = add_styles(activities)

    return Response(activities, status=status.HTTP_200_OK)


def get_questions_per_sentence(sentences):
    questions_sentence = []
    for sen in sentences:
        questions_sentence.append({
            'questions': get_questions(sen.sentence),
            'word': UserSentenceModelSerializer(sen).data
        })

    result = []
    for q_s in questions_sentence:
        for q in q_s['questions']:
            result.append({
                'question': q['question'],
                'word': q_s['word']
            })

    return result


def get_sentences(id):
    all_sentences = list(UserSentence.objects.filter(user__id=id, status=Status.ACTIVE))
    random.shuffle(all_sentences)
    range_total = 4 if len(all_sentences) > 4 else len(all_sentences)
    sentences_obj = [all_sentences[i] for i in range(range_total)]
    # sentences = [sen.sentence for sen in sentences_obj]

    return sentences_obj


def get_questions(sentence):
    words = tokenize_words(str(sentence))
    literal_questions = literal_search(words)

    sentence_blob = TextBlob(sentence)
    sentence_blob = sentence_blob.correct()
    words = tokenize_words(str(sentence_blob))
    refined_questions = refined_search(words)

    phrasal_verbs = extract_phrasal_verbs(sentence)
    phrasal_verbs_questions = literal_search(phrasal_verbs)

    found_questions = combine_unique2(
        [literal_questions, refined_questions, phrasal_verbs_questions])
    return found_questions


def create_activity_package(found_questions):
    activities = []
    found_questions = copy.deepcopy(found_questions)

    if len(found_questions) < 4:
        ids = [q['question']['id'] for q in found_questions]
        questions = Question.objects.exclude(id__in=ids)
        questions_serializer = QuestionModelSerializer(questions, many=True)

        total = 6 - len(found_questions)

        sample_questions = random.sample(questions_serializer.data, round(total/2))

        for q in sample_questions:
            activities.append({
                'question': q,
                'type': 'question',
                'word': None
            })
    else:
        found_questions_activities = []
        for q in found_questions:
            q['type'] = 'question'
            found_questions_activities.append(q)

        sample_found_questions = random.sample(found_questions_activities, 2)
        ids = [q['question']['id'] for q in sample_found_questions]

        questions = Question.objects.exclude(id__in=ids)
        questions_serializer = QuestionModelSerializer(questions, many=True)

        sample_questions = random.sample(questions_serializer.data, 2)

        for q in sample_questions:
            activities.append({
                'question': q,
                'type': 'question',
                'word': None
            })

    sample_found_questions = random.sample(found_questions, 4)
    activities += sample_found_questions
    return activities


def extract_phrasal_verbs(sentence):
    words_raw = re.findall(r"\w+", sentence.strip())

    words = []
    for w in words_raw:
        words.append(WordNetLemmatizer().lemmatize(w, 'v'))

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
            questions_list = Question.objects.filter(
                words__id=word_obj.id)
            for q in questions_list:
                questions.append({
                    'question': QuestionModelSerializer(q).data,
                    'type': 'question',
                    'word': WordModelSerializer(word_obj).data
                })

        except Word.DoesNotExist:
            pass

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
            questions_list = Question.objects.filter(
                words__id=word_obj.id)
            for q in questions_list:
                questions.append({
                    'question': QuestionModelSerializer(q).data,
                    'type': 'question',
                    'word': WordModelSerializer(word_obj).data
                })

        except Word.DoesNotExist:
            pass

    return questions


def combine_unique2(list_to_combine):
    list_to_combine = copy.deepcopy(list_to_combine)

    questions = []
    for l in list_to_combine:
        questions += l

    memory = []
    unique = []

    for item in questions:
        q_id = item['question']['id']
        if q_id not in memory:
            memory.append(q_id)
            unique.append(item)

    new_questions = []
    for q_unique in unique:
        all_questions = list(
            filter(lambda q: q['question']['id'] == q_unique['question']['id'], questions))
        words = []
        for q in all_questions:
            words.append(q['word'])

        words = combine_unique_words([words])
        random.shuffle(words)
        new_questions.append({
            'question': q_unique['question'],
            'word': words[0]
        })

    return new_questions


def combine_unique_words(list_to_combine):
    list = []

    for l in list_to_combine:
        list += l

    memory = []
    unique = []

    for item in list:
        id = item['id']
        if id not in memory:
            memory.append(id)
            unique.append(item)

    return unique


def combine_unique(list_to_combine):
    list_to_combine = copy.deepcopy(list_to_combine)

    list = []
    for l in list_to_combine:
        list += l

    random.shuffle(list)

    memory = []
    unique = []

    for item in list:
        q_id = item['question']['id']
        if q_id not in memory:
            memory.append(q_id)
            unique.append(item)

    return unique


def add_examples(activities):
    word_with_examples = ['smoke', 'stew', 'steep']
    senteces = UserSentence.objects.filter(sentence__in=word_with_examples)

    act_with_examples = []

    if len(senteces) > 0:
        sentences_text = [s.sentence for s in senteces]
        examples = Example.objects.filter(
            word_text__in=sentences_text, type=ActivityTypes.QUESTION)

        if len(examples) >= 2:
            q1 = Question.objects.get(id=examples[0].activity_id)
            w1 = Word(
                id=-1,
                word=senteces[0].sentence
            )
            act_with_examples.append({
                'question': QuestionModelSerializer(q1).data,
                'word': WordModelSerializer(w1).data,
                'example': ExampleModelSerializer(examples[0]).data,
                'type': 'question',
            })

            q2 = Question.objects.get(id=examples[1].activity_id)
            w2 = Word(
                id=-1,
                word=senteces[1].sentence
            )
            act_with_examples.append({
                'question': QuestionModelSerializer(q2).data,
                'word': WordModelSerializer(w2).data,
                'example': ExampleModelSerializer(examples[1]).data,
                'type': 'question',
            })
        elif len(examples) >= 1:
            q1 = Question.objects.get(id=examples[0].activity_id)
            w1 = Word(
                id=-1,
                word=senteces[0].sentence
            )
            act_with_examples.append({
                'question': QuestionModelSerializer(q1).data,
                'word': WordModelSerializer(w1).data,
                'example': ExampleModelSerializer(examples[0]).data,
                'type': 'question',
            })

    return act_with_examples + activities


def add_examples2(activities):
    new_activities = []
    for act in activities:
        new_act = copy.deepcopy(act)
        if act['type'] == 'question' and act['word']:
            try:
                example_obj = Example.objects.get(
                    question_id=act['question']['id'],
                    word_text=act['word']['word']
                )

                serializer = ExampleModelSerializer(example_obj)
                new_act['example'] = serializer.data
                new_activities.append(new_act)

            except Example.DoesNotExist:
                new_activities.append(new_act)
        else:
            new_activities.append(new_act)

    return new_activities


def add_styles(activities):
    new_activities = []
    for act in activities:
        new_act = act

        # if act['type'] == 'question':
        #     act_type = ActivityTypes.QUESTION
        #     act_id = act['question']['id']
        # else:
        #     act_type = ActivityTypes.DESCRIBE_IMAGE
        #     act_id = act['image']['id']

        try:
            style_obj = Style.objects.get(
                question=act['question']['id']
            )

            serializer = StyleModelSerializer(style_obj)
            new_act['style'] = serializer.data
            new_activities.append(new_act)

        except Style.DoesNotExist:
            new_activities.append(act)
    return new_activities


def get_random_questions(excluded_ids, total):
    questions = Question.objects.filter(
        status=Status.ACTIVE).exclude(id__in=excluded_ids)        
    questions = random.sample(list(questions), total)    
    questions_data = QuestionModelSerializer(questions, many=True).data

    for i, q in enumerate(questions):
        ids = q.words.all().values_list('id', flat=True)

        words = Word.objects.filter(
            status=Status.ACTIVE,
            difficulty=Difficulty.EASY,
            id__in=ids
        )

        if len(words) > 0:
            word = random.choice(words)
            questions_data[i]['word'] = WordModelSerializer(word).data

    return questions_data
