from rest_framework import serializers

from users.models import User
from api.models import (
    DescribeImageActivity, UserSentence, Word, QuestionActivity,
    Example, Style
)


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


class WordModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Word
        fields = '__all__'


class QuestionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionActivity
        fields = ['id', 'question', 'image_url', 'voice_url', 'difficulty']


class ImageActivityModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DescribeImageActivity
        fields = ['id', 'image_url']


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
