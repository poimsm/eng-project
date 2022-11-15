from rest_framework import serializers

from users.models import User
from api.models import (
    UserSentence, Word, Question,
    Example, Style, ShortVideo,
    InfoCard, FavoriteResource,
)


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class WordModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Word
        fields = '__all__'


class QuestionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'question', 'image_url', 'voice_url']


class UserSentenceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSentence
        fields = '__all__'


class ExampleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Example
        fields = '__all__'


class StyleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Style
        fields = '__all__'


class ShortVideoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShortVideo
        fields = '__all__'


class InfoCardModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = InfoCard
        fields = '__all__'


class FavoriteResourceModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteResource
        fields = '__all__'
