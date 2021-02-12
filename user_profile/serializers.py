from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ('id', 'fio', 'phone', 'photo', 'email')


class UserProfilePostSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()

    class Meta:
        model = UserProfile
        fields = ('fio', 'phone', 'email')

