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
    path('api/signup', mainAppViews.SignUpView.as_view()),
    path('api/login', mainAppViews.LogInView.as_view()),
    #post get put userprofile data by user id
    url(r'^api/userProfile/(?P<pk>[0-9]+)/$',mainAppViews.UserProfileView.as_view()),    
    path('api/emailCheck', mainAppViews.EmailCheckView.as_view()),
    #get all centres and its data
    path('api/centres', mainAppViews.CentreView.as_view()),
    #get and post and put centre data by user centre id
    url(r'^api/centres/(?P<pk>[0-9]+)/$', mainAppViews.CentreDataView.as_view()),
    #get all parent courses  info (categories matching) ex: Android 
    path('api/courses', mainAppViews.CourseView.as_view()),
    #get course info and array of centres giving this course by Course ID
    url(r'^api/courses/(?P<pk>[0-9]+)/$',mainAppViews.CourseDetailsView.as_view()),
    #post and get array of images of subCourses by subCourse ID
    url(r'^api/subCourseImages/(?P<pk>[0-9]+)/$', mainAppViews.SubCourseImagesView.as_view()),
    #get centre info and array of subCourses that given by the centre using Centre user id
    url(r'^api/centreCourses/(?P<pk>[0-9]+)/$', mainAppViews.SubCourseView.as_view()),
    #get array of subCourse of certain centre using subCourse ID
    url(r'^api/subCourse/(?P<pk>[0-9]+)/$', mainAppViews.SubCourseDetailView.as_view()),
    #get and post array of starting dates using subCourse ID
    url(r'^api/subCourseDates/(?P<pk>[0-9]+)/$', mainAppViews.SubCourseDatesView.as_view()),
    #get and post categories
    path('api/categories', mainAppViews.CategoriesView.as_view()),
    #get array of trending courses
    path('api/trend', mainAppViews.TrendingSubCoursesView.as_view()),
]
urlpatterns += staticfiles_urlpatterns()
