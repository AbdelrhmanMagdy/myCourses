"""myCourses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import include, path, re_path
from django.contrib import admin

from mainApp import views as mainAppViews
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^api/admin/', admin.site.urls),
    url(r'^api/signup', mainAppViews.SignUpView.as_view()),
    url(r'^api/login', mainAppViews.LogInView.as_view()),
    #POST GET PUT userprofile data by USER ID
    url(r'^api/userProfile/(?P<pk>[0-9]+)/$',mainAppViews.UserProfileView.as_view()),    
    url(r'^api/emailCheck', mainAppViews.EmailCheckView.as_view()),
    #GET all centres and its data
    url(r'^api/centres/$', mainAppViews.CentreView.as_view()),
    #GET and POST and PUT centre data by user CENTRE ID
    url(r'^api/centres/(?P<pk>[0-9]+)/$', mainAppViews.CentreDataView.as_view()),
    #GET all parent courses  info (categories matching) ex: Android 
    url(r'^api/courses/$', mainAppViews.CourseView.as_view()),
    url(r'^api/coursesLang/$', mainAppViews.CourseLangView.as_view()),
    #GET course info and array of centres giving this course by COURSE ID
    url(r'^api/courses/(?P<pk>[0-9]+)/$',mainAppViews.CourseDetailsView.as_view()),
    #POST and GET array of images of subCourses by SUBCOURSE ID
    url(r'^api/subCourseImages/(?P<pk>[0-9]+)/$', mainAppViews.SubCourseImagesView.as_view()),
    #GET centre info and array of subCourses that given by the centre using user CENTRE ID
    url(r'^api/centreCourses/(?P<pk>[0-9]+)/$', mainAppViews.SubCourseView.as_view()),
    url(r'^api/deleteCourse/(?P<pk>[0-9]+)/$', mainAppViews.deleteCourseView.as_view()),
    #GET array of subCourse of certain centre using SUBCOURSE ID
    url(r'^api/subCourse/(?P<pk>[0-9]+)/$', mainAppViews.SubCourseDetailView.as_view()),
    #GET and POST array of starting dates using SUBCOURSE ID
    url(r'^api/subCourseDates/(?P<pk>[0-9]+)/$', mainAppViews.SubCourseDatesView.as_view()),
    #GET and POST categories
    url(r'^api/categories/$', mainAppViews.CategoriesView.as_view()),
    #GET array of trending courses
    url(r'^api/trend/$', mainAppViews.TrendingSubCoursesView.as_view()),
    #GET array of recommended courses using USER ID
    url(r'^api/recommended/(?P<pk>[0-9]+)/$', mainAppViews.RecommendedCoursesView.as_view()),
    url(r'^api/promoCodeCheck/(?P<promocode>\w+)/$', mainAppViews.PromoCodeView.as_view()),
    #dashboard
    url(r'^api/booking/(?P<pk>[0-9]+)/$', mainAppViews.BookaingUserAPI.as_view()),
    #mobile app
    url(r'^api/userBooking/(?P<pk>[0-9]+)/$', mainAppViews.GetUserBooking.as_view()),
    url(r'^api/UserPromo/(?P<pk>[0-9]+)/$', mainAppViews.PromoCodeUserView.as_view()),
    # /api/searchCourse?search=russell
    url(r'^api/searchCourse', mainAppViews.CourseSearchView.as_view()),
    #social login
    url(r'^api/socialSignIn/', mainAppViews.SocialSignInView.as_view()),
    url(r'^api/socialSignUp/', mainAppViews.SocialSignUpView.as_view()),

    
]
urlpatterns += staticfiles_urlpatterns()


# title of parent
# instructor name
# starting date
# promo code if exits



# id l user
# id subCourse
# promo code if exist string
# starting date

# promo code api



#user profile image
#social login
#course search api