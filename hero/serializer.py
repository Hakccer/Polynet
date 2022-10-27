from rest_framework import serializers
from django.contrib.auth.admin import User
from hero.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PostSerizlier(serializers.ModelSerializer):
    class Meta:
        model = Poster
        fields = '__all__'


class MessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mess
        fields = '__all__'


class OnlyMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mess
        fields = ['messages']
