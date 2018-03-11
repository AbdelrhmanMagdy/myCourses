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
from .models import UserProfileModel, CoursesModel, DatesModel, SubCourseImagesModel, CentreModel, SubCoursesModel, PromoCodeModel, BookingModel, studyCategoriesModel, PromoCodeUserModel, SocialUsers, MsgSubcourse

# Serializers
from .serializers import UserSerializer, UserProfileSerializer, CentreSerializer, SubCourseImagesSerializer, CoursesSerializer, SubCourseSerializer, CategorySerializer, SubCourseImagesSerializer, StartingDateSerializer, SubCoursePostSerializer, PromoCodeSerializer, BookingSerializer, BookingFinalSerializer, PromoCodeUserSerializer, SocialUsersSerializer, SocialSerializer, UserBookingSerializer, PromoCodeUserPlusSerializer, MsgSubcourseSerializer
# Create your views here.
import markdown
from rest_framework_jwt.settings import api_settings
from django.conf import settings

from rest_framework import generics
from rest_framework import filters
from rest_framework import status



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
        # print(user)
        if user is not None:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)            
            try:
                print(UserProfileModel.objects.get(user__pk=user.id))
                profile = UserProfileModel.objects.get(user__pk=user.id)
            except UserProfileModel.DoesNotExist:
                return Response({"login":"true","is_staff":user.is_staff, "id":user.id,"first_name":user.first_name,"is_superuser":user.is_superuser,'mobile':'',"token":token})
            
            # print(user)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            # print(user)

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({"login":"true","is_staff":user.is_staff, "id":user.id,"first_name":user.first_name,"is_superuser":user.is_superuser,'mobile':profile.mobile,"token":token})
        return Response({"login":"false","is_staff":"", "id":"","first_name":"","is_superuser":"",'mobile':''})


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
            user.first_name=serialized.data['first_name']
            user.save()

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            print(user)
    
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)            
            return Response({"created":"true","id":user.id,"token":token})
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
        return Response({"created":"false","errors":serializer.errors})             
    
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
        return Response({"created":"false","errors":serializer.errors})

class deleteCourseView(APIView):
    def delete(self, request, pk):
        try:
            centre = SubCoursesModel.objects.get(pk=pk)
        except SubCoursesModel.DoesNotExist:
            return Response({"deleted":"false","errors":"this course doesn't exist"})
        centre.delete()
        return Response({"deleted":"true"})
class deleteBookingView(APIView):
    def delete(self, request, pk):
        try:
            book = BookingModel.objects.get(pk=pk)
        except SubCoursesModel.DoesNotExist:
            return Response({"deleted":"false","errors":"this course doesn't exist"})
        book.delete()
        return Response({"deleted":"true"})
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
    def patch(self, request,pk,format=None):
        subCourse = SubCoursesModel.objects.get(pk=pk)
        serializer = SubCoursePostSerializer(subCourse,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"created":"true","id":serializer.data['id']})
        return Response({"created":"false","errors":serializer.errors})


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
class CourseLangView(APIView):
    def get(self, request,format=None):
        courses = CoursesModel.objects.filter(categories__category='language')
        serializer = CoursesSerializer(courses,many=True)
        return Response(serializer.data)
class CourseFilterView(APIView):
    def get(self, request, param,format=None):
        print('////////////////////')
    
        param.replace('%20',' ')
        print(param)
        courses = CoursesModel.objects.filter(categories__category=param)
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
        subcourseSerializer = SubCourseSerializer(subCourses,many=True)
        for x in subcourseSerializer.data:
            # print(x)
            try:
                centrename = CentreModel.objects.get(user__pk=x['centre'])
                ser = CentreSerializer(centrename)
                # print(ser.data)
                x['centreName'] = ser.data['centreName']
                # x['centreName'] = ser['centreName']
            except CentreModel.DoesNotExist:
                pass
            print(x['centre'])
            # x['name'] = x.centre.centreModel.centreName

        data = {"info":dict(courseSerializer.data),"subCourses":subcourseSerializer.data}
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
        return Response({"discount":promocodes.discount,"id":promocodes.pk})
class BookingDeleteAPI(APIView):
    def delete(self, request, pk):
        try:
            books = BookingModel.objects.get(pk=pk)
        except BookingModel.DoesNotExist:
            return Response({"deleted":"false","errors":"this booking doesn't exist"})
        books.delete()
        return Response({"deleted":"true"})    
class BookaingUserAPI(APIView):
    #post for mobile app and get for dashboard
    def post(self, request, pk, format=None):
        request.data['user'] = int(pk)
        promocode = request.data['promoCode']
        booked = BookingModel.objects.filter(user__pk=pk)
        for book in booked:
            if book.subCourse.pk==request.data['subCourse']:
                return Response({"error":"this course is already reserved"})
        if promocode:
            print(promocode)
            try:
                code = PromoCodeModel.objects.get(promoCode=promocode)
                request.data['promoCode']=code.pk
                # print(code)
                users = BookingModel.objects.filter(user__pk=pk)
                for user in users:
                    if user.promoCode == code:
                        return Response({"errors":"promo code is used"})
            except PromoCodeModel.DoesNotExist:
                return Response({"errors":"promo code is invalid"})
        serializer = BookingSerializer(data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            if promocode:
                try:
                    promo =  PromoCodeUserModel.objects.get(promoCode__pk=request.data['promoCode'],user=request.data['user'])
                except PromoCodeUserModel.DoesNotExist:
                    return Response({"errors":"user promo code is invalid"})
                serializer.save()
                promo.delete()
            return Response({"booking":"true"})
        return Response({"errors":"you are already registred in this course","s":serializer.errors})
    def get(self, request, pk, format=None):
        #for dashboard get user by centre
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
# for android app get all bookings
class GetUserBooking(APIView):
    def get(self,request,pk,format=None):
        books = BookingModel.objects.filter(user__pk=pk)
        serilaizer = UserBookingSerializer(books,many=True)
        result = []
        for book in serilaizer.data:
            # print(book['subCourse'])
            book['id']=book['id']
            course = CoursesModel.objects.get(pk=book['subCourse']['course']['id'])
            try:
                centre = CentreModel.objects.get(user__pk=book['subCourse']['centre'])
            except CentreModel.DoesNotExist:
                return Response({"errors":"centre doesn't exists"})
            result.append({"courseName":course.courseName,"courseImage":str(course.courseImage),"startData":book['startingDate'],"centreName":centre.centreName,"id":book['id']})
        return Response(result)

class PromoCodeUserView(APIView):
    def get(self, request, pk, format=None):
        promoCodes = PromoCodeUserModel.objects.filter(user__pk=pk)
        serializer = PromoCodeUserPlusSerializer(promoCodes,many=True)
        return Response(serializer.data)
    def post(self, request, pk, format=None):
        request.data['user'] = pk        
        print(request.data)
        serializer = PromoCodeUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                found = PromoCodeModel.objects.get(pk=request.data['promoCode'])
            except PromoCodeUserModel.DoesNotExist:
                return Response({"errors":"this promo code isn't valid"})
            try:
                obj = PromoCodeUserModel.objects.get(promoCode=request.data['promoCode'],user=request.data['user'])
                print(obj)
                return Response({"errors":"PromoCode is already used"})
            except PromoCodeUserModel.DoesNotExist:
                serializer.save()
                return Response({"created":"true","data":serializer.data})
        return Response({"errors":serializer.errors})

class CourseSearchView(generics.ListAPIView):
    queryset = CoursesModel.objects.all()
    serializer_class = CoursesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('courseName',)



class SocialSignUpView(APIView):

    def post(self, request):

        social_serializer = SocialSerializer(data=request.data)
        social_serializer_email = SocialUsersSerializer(data=request.data)

        if social_serializer_email.is_valid() and social_serializer.is_valid():

            try:
                social_serializer_email.validated_data["email"]
            except KeyError:
                return Response({"error": "Some data is missing"}, status=status.HTTP_400_BAD_REQUEST)

            try:

                SocialUsers.objects.get(socialID=social_serializer.validated_data["socialID"])

            except SocialUsers.DoesNotExist:

                try:
                    User.objects.get(email=social_serializer_email.validated_data["email"])

                except User.DoesNotExist:

                    try:
                        user = User.objects.create_user(username=social_serializer_email.validated_data["email"],
                                                        email=social_serializer_email.validated_data["email"])
                        user.first_name=request.data['first_name']
                        user.save()
                        # print(social_serializer.data)
                        social_serializer.save(user=user)
                    except Exception as e:
                        print('%s (%s)' % (e.message, type(e)))
                        Response({"errors": "Please try again later"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)

                    return Response({"created":"true","id":user.id, "token": token}, status=status.HTTP_201_CREATED)

                else:
                    return Response({"errors": "The Account Already Exists, you should login using your password"},
                                    status=status.HTTP_401_UNAUTHORIZED)

            else:
                return Response({"errors": "Social Account Already Exists!"}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            social_serializer_email.is_valid()
            social_serializer.is_valid()
            errors = social_serializer.errors;
            errors.update(social_serializer_email.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class SocialSignInView(APIView):

    def post(self, request):

        social_serializer = SocialSerializer(data=request.data)
        if social_serializer.is_valid():
            try:
                account = SocialUsers.objects.get(socialID=social_serializer.validated_data["socialID"])
                user = account.user
            except SocialUsers.DoesNotExist:
                return Response({"error": "Social account doesn't exist, Please sign up first"}, status=status.HTTP_401_UNAUTHORIZED)

            else:
                if social_serializer.validated_data["provider"] == account.provider:

                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    try:
                        profile = UserProfileModel.objects.get(user__pk=user.id)
                        return Response({"login":"true","is_staff":user.is_staff, "id":user.id,"first_name":user.first_name,"is_superuser":user.is_superuser,'mobile':profile.mobile,"token":token})
                    except UserProfileModel.DoesNotExist:
                        return Response({"login":"true","is_staff":user.is_staff, "id":user.id,"first_name":user.first_name,"is_superuser":user.is_superuser,'mobile':'',"token":token})
                    # return Response({"created":"true","token": token}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"errors": "Social provider is wrong"}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(social_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DatesUpdateView(APIView):
    def get(self, request, pk, format=None):
        date = DatesModel.objects.filter(pk=pk)
        serializer = StartingDateSerializer(date,many=True)
        return Response(serializer.data)
    def patch(self, request,pk,format=None):
        date = DatesModel.objects.get(pk=pk)
        serializer = StartingDateSerializer(date,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"created":"true","id":serializer.data})
        return Response({"created":"false","errors":serializer.errors})

class MsgSubcourseView(APIView):
    # post msgsubcourse model
    def post(self, request, pk, format=None):
        request.data['subCourse'] = pk
        serializer = MsgSubcourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"created":"True"})    
        return Response({"created":"False","errors":serializer.errors})    
    # get tokens of booked users using id of the subcourse
    def get(self, request, pk, format=None):
        bookedUsers = BookingModel.objects.filter(subCourse__pk=pk)
        tokens = []
        print(bookedUsers)
        for user in bookedUsers:
            tokens.append(user.user.userProfile.reg_token)
        print(tokens)
        return Response({"data":tokens})   

class subCourseMsgView(APIView):
    # given forign keys of users  and get MSGs object by thier booked subcourse
    def post(self,request, format=None):
        subcourses = request.data
        data = {}
        for subcourse in subcourses:
            bookedCourses = MsgSubcourse.objects.filter(subCourse__pk=subcourse)
            serializer = MsgSubcourseSerializer(bookedCourses, many=True)
            data[subcourse] = serializer.data
        return Response({"data":data})   
        