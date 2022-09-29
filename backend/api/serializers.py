from rest_framework import serializers

from users.models import User
from api.models import DescribeImageActivity, Word, QuestionActivity


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
        fields = ['id', 'question', 'image_url', 'difficulty']

class ImageActivityModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DescribeImageActivity
        fields = ['id', 'image_url']

