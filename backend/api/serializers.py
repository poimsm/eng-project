from rest_framework import serializers

from users.models import User
from api.models import Word, Question


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
        model = Question
        fields = ['id', 'question']
