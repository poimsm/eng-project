from rest_framework import serializers

from users.models import User
from api.models import ImageActivity, Word, Question


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
        fields = ['id', 'question', 'image_url', 'difficulty']

class ImageActivityModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ImageActivity
        fields = ['id', 'image_url']

