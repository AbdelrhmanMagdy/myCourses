# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
# Important packages
from rest_framework.views import APIView
from rest_framework.response import Response

# Models
from .models import UserProfileModel
from django.contrib.auth.models import User

# Serializers
from .serializers import UserSerializer,UserProfileSerializer
# Create your views here.

class UserView(APIView):
    def post(self,request):
        userSerializer = UserSerializer(data=request.data)
        if userSerializer.is_valid():
            userSerializer.save()
            return Response({"created":"true"})
        return Response(userSerializer.errors)

class UserProfileView(APIView):

    def get(self, request, format=None):
        users = UserProfileModel.objects.all()
        serializer = UserProfileSerializer(users, many = True)
        return Response(serializer.data)
    def post(self, request):
        user = User.objects.get(username=request.data['username'])
        print(user)
        request.date['user']=user.id 
        print(request.data['user']) 
        profileSerializer = UserProfileSerializer(data = request.data)
        if profileSerializer.is_valid():
            return Response(profileSerializer.data)
        return Response(profileSerializer.errors)