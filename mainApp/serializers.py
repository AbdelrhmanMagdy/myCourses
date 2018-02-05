from rest_framework import serializers
from .models import UserProfileModel
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = ('mobile','educationLevel','major','university','faculty')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('password', 'username',)

class 