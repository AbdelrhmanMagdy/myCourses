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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('signup', mainAppViews.SignUpView.as_view()),
    path('login', mainAppViews.LogInView.as_view()),
    path('userProfile', mainAppViews.UserProfileView.as_view()),
    path('emailCheck', mainAppViews.EmailCheckView.as_view()),
    path('api/centres', mainAppViews.CentreView.as_view()),
    path('api/courses', mainAppViews.CourseView.as_view()),
     url(r'^api/courses/(?P<pk>[0-9]+)/$',mainAppViews.CourseDetailsView.as_view()),
    url(r'^api/centreImages/(?P<pk>[0-9]+)/$', mainAppViews.CentreImagesView.as_view()),
    url(r'^api/centreCourses/(?P<pk>[0-9]+)/$', mainAppViews.SubCourseView.as_view()),

]
