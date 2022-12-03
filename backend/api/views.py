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
from rest_framework.serializers import ValidationError
from django.db import transaction, IntegrityError


# Data
from api.data.common_words import common_words_list
from api.data.phrasal_verbs import phrasal_verbs
from api.data.slangs import slangs
from api.data.expresions import expresions
from api.constants import AppMsg

# Models & serializers
from users.models import User
from api.models import (
    Word, Question, QuestionTypes,
    UserSentence, Example, Style, ShortVideo,
    InfoCard, FavoriteResource, SourceTypes,
    SentenceTypes, SentenceOrigin, ResourceSentence,
    Status, Difficulty, Collocation, UserProfile
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
    QuestionFullSerializer,
    CollocationModelSerializer,
    ResourceSentenceModelSerializer,
    ResourceSentenceSmallModelSerializer,
    UserScreenFlowModelSerializer,
    UserProfileModelSerializer,
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


logger = logging.getLogger('api_v1')
test_user_id = 1
appMsg = AppMsg()


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([permissions.IsAuthenticated])
def user_data(request):

    try:
        user = UserProfile.objects.get(user=request.user.id)
        serializer = UserProfileModelSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as err:
        logger.error(err)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def user_register(request):
    try:
        data = request.data.copy()
        with transaction.atomic():
            user_serializer = UserModelSerializer(data={
                'email': data['email'],
                'password': make_password(
                    data['password'], salt=None, hasher='default'),
                'verified': False,
                'email': data['email'],
            })
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

            profile_serializer = UserProfileModelSerializer(data={
                'email': data['email'],
                'user': user_serializer.data['id']
            })
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

        class UserPayload:
            id = user_serializer.data['id']

        refresh = CustomTokenObtainPairSerializer().get_token(UserPayload)

        return Response({
            'user': profile_serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    except Exception as err:
        logger.error(err)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def hola(request):
    # data = get_random_questions([12], 3)

    # sentence = UserSentence(
    #     id=1,
    #     sentence='asdasd',
    #     meaning='asdad',
    #     origin=1,
    #     type=1,
    #     sourceType=1,
    #     info_card=1,
    #     short_video=1,
    # )

    sentence = UserSentence(
        id=1,
        sentence='asdasd',
        meaning='asdad',
        origin=1,
        type=1,
        source_type=1,
        # info_card=1,
    )

    sentence.info_card = 1

    ser = UserSentenceModelSerializer(sentence)

    return Response(ser.data, status=status.HTTP_200_OK)

    # username = uuid.uuid4().hex[:10]
    # email = username + '@fake.com'
    # password = username

    # data = {
    #     'username': username,
    #     'email': email,
    #     'password': password,
    # }

    # return Response(data, status=status.HTTP_200_OK)

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


@api_view(['GET', 'PUT'])
@renderer_classes([JSONRenderer])
def short_video(request):
    if request.method == 'GET':
        videos = ShortVideo.objects.all().order_by('-created')
        user_videos = FavoriteResource.objects.filter(
            source_type=SourceTypes.SHORT_VIDEO,
            user=1,
            status=Status.ACTIVE,
        )

        result = []
        for video in videos:
            is_favorite = False
            for user_vid in user_videos:
                if video.id == user_vid.short_video.id:
                    is_favorite = True

            sentences = ResourceSentence.objects.filter(
                short_video=video.id,
                status=Status.ACTIVE
            )

            collocations = Collocation.objects.filter(
                short_video=video.id,
                status=Status.ACTIVE
            )

            collocationStringList = [col.text for col in collocations]

            result.append({
                'id': video.id,
                'cover': video.cover,
                'url': video.url,
                'is_favorite': is_favorite,
                'sentences': ResourceSentenceSmallModelSerializer(
                    sentences, many=True).data,
                'collocations': collocationStringList
            })

        return Response(result, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        data = request.data.copy()

        if data['is_favorite']:
            resource_data = {
                'user': 1,
                'short_video': data['id'],
                'source_type': SourceTypes.SHORT_VIDEO,
            }

            resource_serializer = FavoriteResourceModelSerializer(
                data=resource_data)
            resource_serializer.is_valid(raise_exception=True)
            resource_serializer.save()

            sentences = ResourceSentence.objects.filter(
                short_video=data['id'],
                status=Status.ACTIVE
            )

            for sen in sentences:
                sen_data = {
                    'sentence': sen.sentence,
                    'meaning': sen.meaning,
                    'extras': sen.extras,
                    'type': sen.type,
                    'origin': SentenceOrigin.RESOURCE,
                    'short_video': data['id'],
                    'source_type': SourceTypes.SHORT_VIDEO,
                    'user': 1,
                }

                user_sen_serializer = UserSentenceModelSerializer(
                    data=sen_data)
                user_sen_serializer.is_valid(raise_exception=True)
                user_sen_serializer.save()

            return Response({'is_favorite': True}, status=status.HTTP_200_OK)
        else:
            FavoriteResource.objects.filter(
                user=1,
                short_video=data['id']
            ).update(status=Status.DELETED)

            UserSentence.objects.filter(
                user=1,
                short_video=data['id'],
            ).update(status=Status.DELETED)
            return Response({'is_favorite': False}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@renderer_classes([JSONRenderer])
def info_card(request):
    if request.method == 'GET':

        existing_groups = [1, 2]
        group = random.choice(existing_groups)

        cards = InfoCard.objects.filter(
            group=group
        ).order_by('-created')

        user_cards = FavoriteResource.objects.filter(
            source_type=SourceTypes.INFO_CARD,
            user=1,
            status=Status.ACTIVE
        )

        result = []
        for card in cards:
            is_favorite = False

            for user_card in user_cards:
                if card.id == user_card.info_card.id:
                    is_favorite = True
                    break

            sentences = ResourceSentence.objects.filter(
                info_card=card.id,
                status=Status.ACTIVE
            )

            collocations = Collocation.objects.filter(
                info_card=card.id,
                status=Status.ACTIVE
            )

            collocationStringList = [col.text for col in collocations]

            result.append({
                'id': card.id,
                'image_url': card.image_url,
                'voice_url': card.voice_url,
                'is_favorite': is_favorite,
                'sentences': ResourceSentenceSmallModelSerializer(
                    sentences, many=True).data,
                'collocations': collocationStringList
            })

        random.shuffle(result)

        return Response(result, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        data = request.data.copy()

        if data['is_favorite']:
            resource_data = {
                'user': 1,
                'info_card': data['id'],
                'source_type': SourceTypes.INFO_CARD,
            }

            resource_serializer = FavoriteResourceModelSerializer(
                data=resource_data)

            resource_serializer.is_valid(raise_exception=True)
            resource_serializer.save()

            sentences = ResourceSentence.objects.filter(
                info_card=data['id'],
                status=Status.ACTIVE
            )

            for sen in sentences:
                sen_data = {
                    'sentence': sen.sentence,
                    'meaning': sen.meaning,
                    'extras': sen.extras,
                    'type': sen.type,
                    'origin': SentenceOrigin.RESOURCE,
                    'info_card': data['id'],
                    'source_type': SourceTypes.INFO_CARD,
                    'user': 1,
                }

                user_sen_serializer = UserSentenceModelSerializer(
                    data=sen_data)
                user_sen_serializer.is_valid(raise_exception=True)
                user_sen_serializer.save()

            return Response({'is_favorite': True}, status=status.HTTP_200_OK)

        else:
            FavoriteResource.objects.filter(
                user=1,
                info_card=data['id']
            ).update(status=Status.DELETED)

            UserSentence.objects.filter(
                user=1,
                info_card=data['id']
            ).update(status=Status.DELETED)
            return Response({'is_favorite': False}, status=status.HTTP_200_OK)


@api_view(['POST'])
def screen_flow(request):
    data = request.data.copy()

    serializer = UserScreenFlowModelSerializer(data={
        'type': data.get('type', None),
        'user': 1
    })

    if serializer.is_valid():
        serializer.save()

    return Response({}, status=status.HTTP_200_OK)


@api_view(['POST'])
def convert_local_sentences(request):
    data = request.data.copy()
    local_sentences = data['local_sentences']

    result = []
    for local in local_sentences:
        sentence = local
        if local.get('info_card', False):
            card = InfoCard.objects.get(id=local['info_card'])
            sentences = ResourceSentence.objects.filter(
                info_card=card.id,
                status=Status.ACTIVE
            )

            sentence['info_card'] = InfoCardModelSerializer(
                card).data
            sentence['info_card']['sentences'] = ResourceSentenceSmallModelSerializer(
                sentences, many=True).data

            collocations = Collocation.objects.filter(
                info_card=card.id,
                status=Status.ACTIVE
            )

            collocationList = [col.text for col in collocations]
            sentence['info_card']['collocations'] = collocationList

        if local.get('short_video', False):
            video = ShortVideo.objects.get(id=local['short_video'])
            sentences = ResourceSentence.objects.filter(
                short_video=video.id,
                status=Status.ACTIVE
            )
            sentence['short_video'] = ShortVideoModelSerializer(
                video).data
            sentence['short_video']['sentences'] = ResourceSentenceSmallModelSerializer(
                sentences, many=True).data

            collocations = Collocation.objects.filter(
                short_video=video.id,
                status=Status.ACTIVE
            )

            collocationList = [col.text for col in collocations]
            sentence['short_video']['collocations'] = collocationList

        result.append(sentence)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@renderer_classes([JSONRenderer])
def user_sentences(request):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        per_page = 200

        sentences = UserSentence.objects.filter(
            user__id=test_user_id,
            status=Status.ACTIVE
        ).order_by('-created')

        total = sentences.count()
        start = (page - 1)*per_page
        end = page*per_page

        serializer = UserSentenceModelSerializer(
            sentences[start:end], many=True)

        sentences = serializer.data
        sentences = add_videos_and_cards_into_sentences(sentences)

        return Response({
            'data': sentences,
            'total_items': total,
            'current_page': page,
            'total_pages': math.ceil(total / per_page)
        }, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data.copy()

        if check_for_slangs(data['sentence']):
            return Response(appMsg.OFENSIVE_STATEMENT, status=status.HTTP_400_BAD_REQUEST)

        sentence = {
            'user': 1,
            'sentence': data['sentence'],
            'meaning': data['meaning'] if data['meaning'] else '',
            'type': SentenceTypes.NORMAL,
            'origin': SentenceOrigin.USER
        }

        serializer = UserSentenceModelSerializer(data=sentence)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(appMsg.INVALID_DATA, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        try:
            data = request.data.copy()

            if check_for_slangs(data['sentence']):
                return Response(appMsg.OFENSIVE_STATEMENT, status=status.HTTP_400_BAD_REQUEST)

            sentence = UserSentence.objects.get(id=data.get('id', None))
            serializer = UserSentenceModelSerializer(
                sentence, data=data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(appMsg.INVALID_DATA, status=status.HTTP_400_BAD_REQUEST)

        except UserSentence.DoesNotExist:
            return Response(appMsg.ID_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(e)
            return Response(appMsg.UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'DELETE':
        try:
            sentence = UserSentence.objects.get(id=request.data['id'])
            sentence.status = Status.DELETED
            sentence.save()
            return Response({}, status=status.HTTP_200_OK)
        except UserSentence.DoesNotExist:
            return Response(appMsg.ID_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(e)
            return Response(appMsg.UNKNOWN_ERROR, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def daily_activities_limited(request):

    data = request.data.copy()
    local_sentences = data.get('local_sentences', [])
    logger.debug('aaaaaaaaaaa1')

    logger.debug(local_sentences)

    sentences = convert_local_sentences_to_sentences(local_sentences)
    logger.debug('aaaaaaaaaaa2')
    logger.debug(sentences)

    # all_sentences_are_strings = True;
    # for w in sentences:
    #     if not (isinstance(w, str) and len(w) <= 20) :
    #         all_sentences_are_strings = False
    #         break

    # if not all_sentences_are_strings:
    #     return Response({}, status=status.HTTP_400_BAD_REQUEST)

    # sentences = get_sentences(test_user_id)

    questions = get_questions_per_sentence(sentences)
    logger.debug('aaaaaaaaaaa3')
    logger.debug(questions)
    activities = create_activity_package(questions)
    logger.debug('aaaaaaaaaaa4')
    logger.debug(activities)
    activities = add_examples(activities)
    logger.debug('aaaaaaaaaaa5')
    logger.debug(activities)
    activities = add_styles(activities)
    logger.debug('aaaaaaaaaaa6')
    logger.debug(activities)
    activities = add_videos_and_cards(activities)
    logger.debug('aaaaaaaaaaa7')

    return Response(activities, status=status.HTTP_200_OK)


def get_sentences(id):
    all_sentences = list(UserSentence.objects.filter(
        user__id=id, status=Status.ACTIVE))
    random.shuffle(all_sentences)
    range_total = 10 if len(all_sentences) > 10 else len(all_sentences)
    sentences_obj = [all_sentences[i] for i in range(range_total)]

    return sentences_obj


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def daily_activities(request):

    sentences = get_sentences(test_user_id)
    questions = get_questions_per_sentence(sentences)
    activities = create_activity_package(questions)
    activities = add_examples(activities)
    activities = add_styles(activities)
    activities = add_videos_and_cards(activities)

    return Response(activities, status=status.HTTP_200_OK)


def get_sentences(id):
    all_sentences = list(UserSentence.objects.filter(
        user__id=id, status=Status.ACTIVE))
    random.shuffle(all_sentences)
    range_total = 10 if len(all_sentences) > 10 else len(all_sentences)
    sentences_obj = [all_sentences[i] for i in range(range_total)]

    return sentences_obj


def get_questions_per_sentence(sentences):
    questions_sentence = []
    for sen in sentences:
        questions_sentence.append({
            'questions': get_questions(sen.sentence),
            'sentence': UserSentenceModelSerializer(sen).data
        })

    memory = []
    result = []
    for q_s in questions_sentence:
        for q in q_s['questions']:
            if q_s['sentence'] in memory:
                continue

            if len(result) > 6:
                break

            result.append({
                'question': q['question'],
                'sentence': q_s['sentence']
            })
            memory.append(q_s['sentence'])

    return result


def get_questions(sentence):
    sentences = tokenize_sentences(str(sentence))
    literal_questions = literal_search(sentences)

    sentence_blob = TextBlob(sentence)
    sentence_blob = sentence_blob.correct()
    sentences = tokenize_sentences(str(sentence_blob))
    refined_questions = refined_search(sentences)

    phrasal_verbs = extract_phrasal_verbs(sentence)
    phrasal_verbs_questions = literal_search(phrasal_verbs)

    found_questions = combine_unique2(
        [literal_questions, refined_questions, phrasal_verbs_questions])

    if len(found_questions) == 0:
        questions = Question.objects.filter(type=QuestionTypes.NORMAL)
        q = random.choice(questions)

        found_questions.append({
            'question': QuestionModelSerializer(q).data,
            'sentence': None
        })
    return found_questions


def create_activity_package(found_questions):
    found_questions = copy.deepcopy(found_questions)

    result = []

    if len(found_questions) == 0:
        easy_questions, ids = get_easy_questions_with_examples(2)
        random_questions = get_random_questions(ids, 4)
        gap_questions = random_questions + found_questions
        random.shuffle(gap_questions)
        result = easy_questions + gap_questions
    elif len(found_questions) < 6:
        ids = [q['question']['id'] for q in found_questions]
        total = 6 - len(found_questions)
        result = found_questions + get_random_questions(ids, total)
        random.shuffle(result)
    else:
        found_questions = random.sample(found_questions, 6)
        # ids = [q['question']['id'] for q in found_questions]
        # result = found_questions + get_random_questions(ids, 2)
        result = found_questions
        random.shuffle(result)

    hasDescribeImg = False
    for r in result:
        if r['question']['type'] == QuestionTypes.DESCRIBE_IMAGE:
            hasDescribeImg = True
            break

    if not hasDescribeImg:
        questions = Question.objects.filter(type=QuestionTypes.DESCRIBE_IMAGE)
        q = random.choice(questions)

        result[4] = {
            'question': QuestionModelSerializer(q).data,
            'sentence': None
        }

    return result


def extract_phrasal_verbs(sentence):
    sentences_raw = re.findall(r"\w+", sentence.strip())

    sentences = []
    for w in sentences_raw:
        sentences.append(WordNetLemmatizer().lemmatize(w, 'v'))

    possible_match = []
    for v in phrasal_verbs:
        verb = v.split('_')[0]
        for sentence in sentences:
            if sentence == verb:
                if sentence not in possible_match:
                    possible_match.append({
                        'sentence': sentence,
                        'phrasal_verb': v,
                        'end': v.split('_')[1]
                    })

    matches = []
    for m in possible_match:
        for w in sentences:
            if w == m['end']:
                if m['phrasal_verb'] not in matches:
                    matches.append(m['phrasal_verb'])
    return matches


def check_for_slangs(sentence):
    sentences = re.findall(r"\w+", sentence.strip())
    sentences = filter(lambda w: w.lower() in slangs, sentences)
    return len(list(sentences)) != 0


def tokenize_sentences(sentence):
    sentences = re.findall(r"\w+", sentence.strip())
    sentences = filter(lambda w: len(w) > 2, sentences)
    sentences = filter(lambda w: not w.lower() in common_words_list, sentences)
    return list(sentences)


def literal_search(sentences):
    questions = []
    for sentence in sentences:
        try:
            word_obj = Word.objects.get(word=sentence)
            questions_list = Question.objects.filter(
                words__id=word_obj.id)
            for q in questions_list:
                questions.append({
                    'question': QuestionModelSerializer(q).data,
                    'sentence': WordModelSerializer(word_obj).data
                })

        except Word.DoesNotExist:
            pass
        except Exception as e:
            logger.exception(e)

    return questions


def refined_search(sentences):
    all_forms = set()
    for sentence in sentences:
        forms = get_word_forms(sentence)
        all_forms = all_forms | forms['n'] | forms['a'] | forms['v'] | forms['r']

    questions = []
    for sentence in all_forms:
        try:
            sentence_obj = sentence.objects.get(sentence=sentence)
            questions_list = Question.objects.filter(
                sentences__id=sentence_obj.id)
            for q in questions_list:
                questions.append({
                    'question': QuestionModelSerializer(q).data,
                    'sentence': WordModelSerializer(sentence_obj).data
                })

        except sentence.DoesNotExist:
            pass
        except Exception as e:
            logger.exception(e)

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
        sentences = []
        for q in all_questions:
            sentences.append(q['sentence'])

        sentences = combine_unique_sentences([sentences])
        random.shuffle(sentences)
        new_questions.append({
            'question': q_unique['question'],
            'sentence': sentences[0]
        })

    return new_questions


def combine_unique_sentences(list_to_combine):
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
    new_activities = []
    for act in activities:
        new_act = copy.deepcopy(act)
        if act['sentence']:
            try:
                example_obj = Example.objects.get(
                    question=act['question']['id'],
                    sentence_text=act['sentence']['sentence']
                )

                serializer = ExampleModelSerializer(example_obj)
                new_act['example'] = serializer.data
                new_activities.append(new_act)

            except Example.DoesNotExist:
                new_activities.append(new_act)
            except Exception as e:
                logger.exception(e)
                new_activities.append(new_act)
        else:
            new_activities.append(new_act)

    return new_activities


def add_styles(activities):
    new_activities = []
    for act in activities:
        new_act = act
        try:
            style_obj = Style.objects.get(
                question=act['question']['id']
            )

            serializer = StyleModelSerializer(style_obj)
            new_act['style'] = serializer.data
            new_activities.append(new_act)

        except Style.DoesNotExist:
            new_activities.append(act)
        except Exception as e:
            logger.exception(e)
            new_activities.append(act)
    return new_activities


def add_videos_and_cards(activities):
    new_activities = []
    for act in activities:
        new_act = act
        try:
            if act['sentence'] and act['sentence']['info_card']:
                card = InfoCard.objects.get(id=act['sentence']['info_card'])
                sentences = ResourceSentence.objects.filter(
                    info_card=card.id,
                    status=Status.ACTIVE
                )

                new_act['sentence']['info_card'] = InfoCardModelSerializer(
                    card).data
                new_act['sentence']['info_card']['sentences'] = ResourceSentenceSmallModelSerializer(
                    sentences, many=True).data

                collocations = Collocation.objects.filter(
                    info_card=card.id,
                    status=Status.ACTIVE
                )

                collocationList = [col.text for col in collocations]
                new_act['sentence']['info_card']['collocations'] = collocationList

            if act['sentence'] and act['sentence']['short_video']:
                video = ShortVideo.objects.get(
                    id=act['sentence']['short_video'])
                sentences = ResourceSentence.objects.filter(
                    short_video=video.id,
                    status=Status.ACTIVE
                )
                new_act['sentence']['short_video'] = ShortVideoModelSerializer(
                    video).data
                new_act['sentence']['short_video']['sentences'] = ResourceSentenceSmallModelSerializer(
                    sentences, many=True).data

                collocations = Collocation.objects.filter(
                    short_video=video.id,
                    status=Status.ACTIVE
                )

                collocationList = [col.text for col in collocations]
                new_act['sentence']['short_video']['collocations'] = collocationList

            new_activities.append(new_act)

        except Exception as e:
            logger.exception(e)
            new_activities.append(act)
    return new_activities


def add_videos_and_cards_into_sentences(sentences):
    result = []
    for sen in sentences:
        new_sen = sen
        try:
            if sen['info_card']:
                card = InfoCard.objects.get(id=sen['info_card'])
                sentences = ResourceSentence.objects.filter(
                    info_card=card.id,
                    status=Status.ACTIVE
                )

                new_sen['info_card'] = InfoCardModelSerializer(
                    card).data
                new_sen['info_card']['sentences'] = ResourceSentenceSmallModelSerializer(
                    sentences, many=True).data

                collocations = Collocation.objects.filter(
                    info_card=card.id,
                    status=Status.ACTIVE
                )

                collocationList = [col.text for col in collocations]
                new_sen['info_card']['collocations'] = collocationList

            if sen['short_video']:
                video = ShortVideo.objects.get(id=sen['short_video'])
                sentences = ResourceSentence.objects.filter(
                    short_video=video.id,
                    status=Status.ACTIVE
                )
                new_sen['short_video'] = ShortVideoModelSerializer(
                    video).data
                new_sen['short_video']['sentences'] = ResourceSentenceSmallModelSerializer(
                    sentences, many=True).data

                collocations = Collocation.objects.filter(
                    short_video=video.id,
                    status=Status.ACTIVE
                )

                collocationList = [col.text for col in collocations]
                new_sen['short_video']['collocations'] = collocationList

            result.append(new_sen)

        except Exception as e:
            logger.exception(e)
            result.append(sen)
    return result


def get_easy_questions_with_examples(total):
    questions = list(Question.objects.filter(
        status=Status.ACTIVE,
        difficulty=Difficulty.EASY
    ))

    random.shuffle(questions)

    result = []
    ids = []
    counter = 0

    for q in questions:
        word_ids = q.words.all().values_list('id', flat=True)

        words = list(Word.objects.filter(
            status=Status.ACTIVE,
            difficulty=Difficulty.EASY,
            id__in=word_ids
        ))

        if len(words) == 0:
            continue

        random.shuffle(words)
        sentence = None

        for w in words:
            example = Example.objects.filter(
                status=Status.ACTIVE,
                question=q.id,
                sentence_text=w.word
            ).first()

            if example:
                counter += 1
                sentence = {
                    'id': -1,
                    'origin': SentenceOrigin.RANDOM,
                    'type': SentenceTypes.NORMAL,
                    'sentence': w.word,
                    'meaning': w.meaning
                }
                result.append({
                    'question': QuestionModelSerializer(q).data,
                    'sentence': sentence
                })
                ids.append(q.id)
                if counter == total:
                    break

        if counter == total:
            break

    return result, ids


def get_easy_questions(total):
    questions = Question.objects.filter(
        status=Status.ACTIVE,
        difficulty=Difficulty.EASY
    )
    questions = random.sample(list(questions), total)

    result = []
    ids = []

    for q in questions:
        ids.append(q.id)
        ids = q.words.all().values_list('id', flat=True)

        sentences = Word.objects.filter(
            status=Status.ACTIVE,
            difficulty=Difficulty.EASY,
            id__in=ids
        )

        sentence = None

        if len(sentences) > 0:
            sentence = random.choice(sentences)
            sentence = {
                'id': -1,
                'origin': SentenceOrigin.RANDOM,
                'type': SentenceTypes.NORMAL,
                'sentence': sentence.sentence,
                'meaning': sentence.meaning
            }

        result.append({
            'question': QuestionModelSerializer(q).data,
            'sentence': sentence
        })

    return result, ids


def get_random_questions(excluded_ids, total):
    questions = Question.objects.filter(
        status=Status.ACTIVE).exclude(id__in=excluded_ids)
    questions = random.sample(list(questions), total)

    result = []

    for q in questions:
        ids = q.words.all().values_list('id', flat=True)

        words = Word.objects.filter(
            status=Status.ACTIVE,
            difficulty=Difficulty.EASY,
            id__in=ids
        )

        sentence = None

        if len(words) > 0:
            word = random.choice(words)
            sentence = {
                'id': -1,
                'origin': SentenceOrigin.RANDOM,
                'type': SentenceTypes.NORMAL,
                'sentence': word.word,
                'meaning': word.meaning
            }

        result.append({
            'question': QuestionModelSerializer(q).data,
            'sentence': sentence
        })

    return result


def convert_local_sentences_to_sentences(local_sentences):
    # id: 4, sentence: Smoke, origin: 2, type: 0,
    # meaning: , saved: true,
    # extras: null, sourceType: null, infoCard: null, shortVideo: null

    result = []
    for local in local_sentences:
        sentence = None

        if local.get('info_card', False):
            card = InfoCard.objects.get(id=local['info_card'])

            sentence = UserSentence(
                id=local['id'],
                sentence=local['sentence'],
                meaning=local['meaning'],
                origin=local['origin'],
                type=local['type'],
                source_type=local['source_type'],
                info_card=card
            )

        elif local.get('short_video', False):
            video = ShortVideo.objects.get(id=local['short_video'])

            sentence = UserSentence(
                id=local['id'],
                sentence=local['sentence'],
                meaning=local['meaning'],
                origin=local['origin'],
                type=local['type'],
                source_type=local['source_type'],
                short_video=video
            )

        else:
            sentence = UserSentence(
                id=local['id'],
                sentence=local['sentence'],
                meaning=local['meaning'],
                origin=local['origin'],
                type=local['type'],
                source_type=local['source_type']
            )

        if sentence:
            result.append(sentence)
    return result
