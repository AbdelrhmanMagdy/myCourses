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
from .models import UserProfileModel, CoursesModel, DatesModel, SubCourseImagesModel, CentreModel, SubCoursesModel, PromoCodeModel, BookingModel, studyCategoriesModel

# Serializers
from .serializers import UserSerializer, UserProfileSerializer, CentreSerializer, SubCourseImagesSerializer, CoursesSerializer, SubCourseSerializer, CategorySerializer, SubCourseImagesSerializer, StartingDateSerializer, SubCoursePostSerializer, PromoCodeSerializer, BookingSerializer, BookingFinalSerializer
# Create your views here.
import markdown

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
        print(user)
        if user is not None:
    	    return Response({"login":"true","is_staff":user.is_staff, "id":user.id,"first_name":user.first_name,"is_superuser":user.is_superuser})
        return Response({"login":"false","errors":"Username or Password isn't correct","request":request.data})


class SignUpView(APIView):
    def post(self,request):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            user = User.objects.create_user(
                serialized.data['username'],
                serialized.data['password']
            )
            user.set_password(serialized.data['password'])
            user.email=serialized.data['username']
            user.save()
            return Response({"created":"true","id":user.id})
        return Response(serialized.errors)

class UserProfileView(APIView):
    def get(self, request,pk, format=None):
        try:
            user = UserProfileModel.objects.get(user__pk=pk)
        except UserProfileModel.DoesNotExist:
            return Response({"errors":"user profile doesn't exist"})
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    def post(self, request,pk,format=None):
        profileSerializer = UserProfileSerializer(data = request.data)
        request.data['user'] = pk
        if profileSerializer.is_valid():
            profileSerializer.save()
            return Response({"created":"true"})
        return Response(profileSerializer.errors)
    def patch(self, request,pk,format=None):
        request.data['user'] = pk
        profile = UserProfileModel.objects.get(user__pk=pk)
        profileSerializer = UserProfileSerializer(profile,data = request.data,partial=True)
        if profileSerializer.is_valid():
            profileSerializer.save()
            return Response({"created":"true"})
        return Response(profileSerializer.errors)
class CentreView(APIView):
    """
        ***GET :***\n
        `<= centres:[]`
        ***POST :***\n
        `=>centres:{}`
    """
    def get(self, request, format=None):
        centres =  CentreModel.objects.all()
        serializer = CentreSerializer(centres,many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = CentreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class CentreDataView(APIView):
    """
        ***GET :***\n
        `centre user id <= centre info:{}`
        ***POST :***\n
        `centre user id =>centres info:{}`
    """    
    def get(self, request, pk, format=None):
        try:
            info =  CentreModel.objects.get(user__pk = pk)
        except CentreModel.DoesNotExist:
            return Response({"errors":"error with centre id"})
        serializer = CentreSerializer(info)
        return Response(serializer.data)
    def post(self, request, pk, format=None):
        request.data['user']=pk
        print(request.data)
        serializer = CentreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"created":"true"})
        return Response(serializer.errors)             
    
    def patch(self, request, pk, format=None):
        request.data['user']=pk
        obj = CentreModel.objects.get(user__pk=pk)        
        serializer = CentreSerializer(obj,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"updated":"true"})
        return Response(serializer.errors)     

class SubCourseImagesView(APIView):
    """
        ***GET :***\n
        `=>subCourse_id`\n
        `<= images:[]`
        ***POST :***\n
        `=>subCourse_id`\n
        `=> images:[]`
    """
    def get(self, request, pk, format=None):
        images =  SubCourseImagesModel.objects.filter(subCourse__pk = pk)
        serializer = SubCourseImagesSerializer(images,many=True)
        return Response(serializer.data)
    def post(self, request, pk, format=None):
        for x in request.data:
            print(x)
            x['subCourse'] = pk    
        serializer = SubCourseImagesSerializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)    

class SubCourseView(APIView):
    """
        ***GET :***\n
        `=>centre_user_id`\n
        `<= courses:[], centre info`
    """
    def get(self, request,pk, format=None):
        try:
            centreInfo = CentreModel.objects.get(user__pk=pk)
        except CentreModel.DoesNotExist:
            return Response({"errors":"centre data doesn't exist"})
        centreInfoSerializer = CentreSerializer(centreInfo)
        subcourses = SubCoursesModel.objects.filter(centre__pk=pk)
        subCoursesSerializer = SubCourseSerializer(subcourses, many=True)
        data= {"courses":[]}
        data["info"]=dict(centreInfoSerializer.data)
        for x in subCoursesSerializer.data:
            data["courses"].append(dict(x))
        return Response(data)
    def post(self,request,pk,format=None):
        request.data['centre']=pk
        serializer = SubCoursePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"created":"true","id":serializer.data['id']})
        return Response(serializer.errors)
class SubCourseDetailView(APIView):
    """
        ***GET :***\n
        `=>subCourse_id`\n
        `<= subCourse info`
    """
    def get(self,request,pk,format=None):
        courseInfo = SubCoursesModel.objects.filter(pk=pk)
        serializer = SubCourseSerializer(courseInfo,many=True)
        return Response(serializer.data)


class CourseView(APIView):
    """
        ***GET :***\n
        `=>course`\n
        `<= course info:{}`
    """
    def get(self, request,format=None):
        courses = CoursesModel.objects.all()
        serializer = CoursesSerializer(courses,many=True)
        return Response(serializer.data)

class CourseDetailsView(APIView):
    """
        ***GET :***\n
        `=>course id`\n
        `<= centres:[], course info:{}`
    """
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
    """
        ***GET :***\n
        `categories:[]`\n
        ***POST :***\n
        `categories:[]`
    """
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

class SubCourseDatesView(APIView):
    """
        ***GET :***\n
        `subcourse id dates:[]`\n
        ***POST :***\n
        `dates:[]`
    """ 
    def get(self, request, pk, format=None):
        dates =  DatesModel.objects.filter(subCourse__pk = pk)
        serializer = StartingDateSerializer(dates,many=True)
        return Response(serializer.data)
    def post(self, request, pk, format=None):
        for x in request.data:
            print(x)
            x['subCourse'] = pk
            
        serializer = StartingDateSerializer(data=request.data,many=True)        
        if serializer.is_valid():
            serializer.save()
            return Response({"created":"true"})
        return Response(serializer.errors)   

class TrendingSubCoursesView(APIView):
    """
        ***GET :***\n
        `all trending subcourses: []`\n
    """ 
    def get(self,request,format=None):
        trend = SubCoursesModel.objects.filter(is_trend=True)
        serializer = SubCourseSerializer(trend,many=True)
        if not trend:
            return Response({"errors":"no trend courses available"})
        return Response(serializer.data)

class RecommendedCoursesView(APIView):
    """
        ***GET :***\n
        `all recommended courses filtired by user category: []`\n
    """    
    def get(self, request, pk, format=None):
        try:
            user = UserProfileModel.objects.get(user__pk=pk)
        except UserProfileModel.DoesNotExist:
            return Response({"errors":"user doesn't have categories"})
        categories = user.fieldOfStudy.all()
        cat_id = []
        for x in  categories:
            cat_id.append(x.id)
        courses =  CoursesModel.objects.filter(categories__in=cat_id)
        if not courses:
            return Response({"errors":"no recommended courses available"})
        serializer = CoursesSerializer(courses,many=True)
        return Response(serializer.data)

class PromoCodeView(APIView):
    def get(self, request, promocode, format=None):
        try:
            promocodes = PromoCodeModel.objects.get(promoCode=promocode)
        except PromoCodeModel.DoesNotExist:
            return Response({"errors":"promo code not valid"})
        serializer = PromoCodeSerializer(promocodes)
        return Response({"discount":promocodes.discount})

class BookaingUserAPI(APIView):
    def post(self, request, pk, format=None):
        request.data['user'] = pk
        promocode = request.data['promoCode']
        try:
            code = PromoCodeModel.objects.get(promoCode=promocode)
            request.data['promoCode']=code.pk
            # print(code)
            users = BookingModel.objects.filter(user__pk=pk)
            for user in users:
                if user.promoCode == code:
                    return Response({"errors":"promo code is expired"})
        except PromoCodeModel.DoesNotExist:
            return Response({"errors":"promo code is invalid"})
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"booking":"true"})
        return Response({"errors":"invalid booking"})
    def get(self, request, pk, format=None):
        subcourses = SubCoursesModel.objects.filter(centre__pk=pk)
        print(subcourses)
        arr = []
        for x in subcourses:
            arr.append(x.id)
        books = BookingModel.objects.filter(subCourse__pk__in=arr)
        serializer = BookingFinalSerializer(books,many=True)
        for x in serializer.data:
            try:
                profile = UserProfileModel.objects.get(user__pk=x['user']['id'])
                x['mobile'] = profile.mobile
            except UserProfileModel.DoesNotExist:
                x['mobile']=''
                pass
        return Response(serializer.data)