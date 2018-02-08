# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
# Important packages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
# Models
from .models import UserProfileModel
from django.contrib.auth.models import User
from .models import CertificatesModel, UserProfileModel, CoursesModel, DatesModel, SubCourseImagesModel, CentreModel, SubCoursesModel, PromoCodeModel, BookingModel, studyCategoriesModel

# Serializers
from .serializers import UserSerializer, UserProfileSerializer, CentreSerializer, SubCourseImagesSerializer, CoursesSerializer, SubCourseSerializer, CategorySerializer, SubCourseImagesSerializer
# Create your views here.


class EmailCheckView(APIView):
    def post(self,request):
        try:
            email = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response({"exist":"false"})    
        return Response({"exist":"true"})    

class LogInView(APIView):
    def post(self,request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            return Response({"login":"true","is_staff":user.is_staff, "id":user.id,"first_name":user.first_name,"is_superuser":user.is_superuser})
        return Response({"login":"false","errors":"Username or Password isn't correct"})


class SignUpView(APIView):
    def post(self,request):
        userSerializer = UserSerializer(data=request.data)
        if userSerializer.is_valid():
            userSerializer.save()
            user = User.objects.get(username=userSerializer.data['username'])
            user.email = userSerializer.data['username']
            user.save()
            # print(email)
            
            return Response({"created":"true","id":user.id})
        return Response(userSerializer.errors)

class UserProfileView(APIView):

    def get(self, request, format=None):
        users = UserProfileModel.objects.all()
        serializer = UserProfileSerializer(users, many = True)
        return Response(serializer.data)
    def post(self, request):
        profileSerializer = UserProfileSerializer(data = request.data)
        if profileSerializer.is_valid():
            profileSerializer.save()
            return Response({"created":"true","id":profileSerializer['user']})
        return Response(profileSerializer.errors)

class CentreView(APIView):

    def get(self, request, format=None):
        centres =  CentreModel.objects.all()
        serializer = CentreSerializer(centres,many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = CentreSerializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



class SubCourseImagesView(APIView):

    def get(self, request, pk, format=None):
        images =  SubCourseImagesModel.objects.filter(subCourse__pk = pk)
        serializer = SubCourseImagesSerializer(images,many=True)
        return Response(serializer.data)
    def post(self, request, pk, format=None):
        serializer = SubCourseImagesSerializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)    

# class CoursesView(APIView):
#     def get(self, request, pk, format=None):
#         centres =  SubCourseImagesModel.objects.filter(centre = pk)
#         serializer = CentreImagesSerializer(centres,many=True)
#         return Response(serializer.data)
#     def post(self, request, pk, format=None):
#         serializer = CentreImagesSerializer(data=request.data,many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)    



class SubCourseView(APIView):
    def get(self, request,pk, format=None):
        centreInfo = CentreModel.objects.get(pk=pk)
        centreInfoSerializer = CentreSerializer(centreInfo)
        subcourses = SubCoursesModel.objects.filter(centre__pk=pk)
        subCoursesSerializer = SubCourseSerializer(subcourses, many=True)
        # subCoursesDates = DatesModel.objects.filter(subCourse__pk=pk)
        # subCoursesDateSerializer = subCoursesDateSerializer(subCoursesDates,many=True)
        data= {"info":[],"courses":[]}
        data["info"].append(dict(centreInfoSerializer.data))
        for x in subCoursesSerializer.data:
            data["courses"].append(dict(x))
        # for x in subCoursesDateSerializer.data:
            # data["dates"].append(dict(x))
        return Response(data)

class CourseView(APIView):
    def get(self, request,format=None):
        courses = CoursesModel.objects.all()
        serializer = CoursesSerializer(courses,many=True)
        return Response(serializer.data)

class CourseDetailsView(APIView):
    def get(self, request,pk,format=None):
        try:
            courses = CoursesModel.objects.get(pk=pk)
        except CoursesModel.DoesNotExist:
            return Response({"error":"course doesn't exist"})
        courseSerializer = CoursesSerializer(courses)
        subCourses = SubCoursesModel.objects.filter(course__pk=pk)
        centres = []
        for course in subCourses:
            centres.append(course.centre)
        centresSerializer = CentreSerializer(centres,many=True)
        data = {"info":dict(courseSerializer.data),"centres":[]}
        for x in centresSerializer.data:
            data["centres"].append(dict(x))
            
        return Response(data)
 
class CategoriesView(APIView):
    def get(self,request,format=None):
        categories = studyCategoriesModel.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer = CategorySerializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

# class SubCourseImagesView(APIView):
#     def post(self,request,format=None):
#         serializer = CentreImagesSerializer(data=request.data,many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)

#     def get(self,request,format=None):
#         images = CentreImagesModel.objects.all()   
#         serializer = CentreImagesSerializer(images,many=True)
#         return Response(serializer.data)