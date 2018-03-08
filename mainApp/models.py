# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class studyCategoriesModel(models.Model):
    category = models.CharField(max_length=90)

    def __str__(self):
        return str(self.category)

class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True, related_name='userProfile')
    mobile = models.CharField(max_length=11)
    fieldOfStudy = models.ManyToManyField(studyCategoriesModel,blank=True,related_name='userCategories') 
    certificate = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='media/userProfiles', blank=True,null=True,default='media/logo.png')
    reg_token = models.TextField(null=True, blank=True)
    def __str__(self):
        return str(self.user)

# class CertificatesModel(models.Model):
    # certificate = models.FileField(upload_to='media/certificates', blank=True,null=True)
    # user = models.ForeignKey(UserProfileModel,on_delete=models.CASCADE, null=True)

class CoursesModel(models.Model):
    courseName = models.CharField(max_length=50)
    courseImage = models.ImageField(upload_to='media/course', blank=True,null=True,default='media/logo.png')
    courseSlogun = models.CharField(max_length=250)
    categories = models.ManyToManyField(studyCategoriesModel,blank=True,related_name='courseCategories') 

    def __str__(self):
        return str(self.courseName)


class CentreModel(models.Model):
    centreName = models.CharField(max_length=50)
    lat = models.FloatField(null=True,blank=True)
    lon = models.FloatField(null=True,blank=True)
    address = models.CharField(max_length=100)
    info = models.CharField(max_length=500)
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE, db_index=True,blank=True, related_name='centreModel' )
    image = models.ImageField(upload_to='media/centre', blank=True,null=True,default='media/logo.png')
    def __str__(self):
        return str(self.centreName)
class SubCoursesModel(models.Model):
    instructorName = models.CharField(max_length=50)
    info = models.CharField(max_length=10000,null=True,blank=True)    
    rate =  models.IntegerField(null=True,blank=True)
    fees = models.CharField(max_length=50)
    course = models.ForeignKey(CoursesModel, on_delete=models.CASCADE, null=True,blank=True, related_name='subCourses')
    centre = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True, related_name='centre')
    is_trend = models.BooleanField(default=False,blank=True)
    def __str__(self):
        return str(self.instructorName)
class DatesModel(models.Model):
    dates = models.DateField()
    subCourse = models.ForeignKey(SubCoursesModel, on_delete=models.CASCADE,null=True,blank=True, related_name='dates')
    
    def __str__(self):
        return str(self.dates)
class SubCourseImagesModel(models.Model):
    images = models.ImageField(upload_to='media/subCourse', blank=True,null=True,default='media/logo.png')
    subCourse = models.ForeignKey(SubCoursesModel, on_delete=models.CASCADE,null=True,blank=True, related_name='images')
    
    def __str__(self):
        return str(self.subCourse.instructorName)

class PromoCodeModel(models.Model):
    promoCode = models.CharField(max_length=50, blank=True,null=True)
    discount = models.IntegerField()
    def __str__(self):
        return str(self.promoCode)
class BookingModel(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE, related_name='booking')
    promoCode = models.ForeignKey(PromoCodeModel, null=True,blank=True,on_delete=models.CASCADE)
    subCourse = models.ForeignKey(SubCoursesModel,on_delete=models.CASCADE, related_name='booking')
    startingDate = models.CharField(max_length=15, null=True, blank=True)
    def __str__(self):
        return str(self.user.username)


class PromoCodeUserModel(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    promoCode = models.ForeignKey(PromoCodeModel, on_delete=models.CASCADE)
    # promoCode = models.CharField(max_length=20, null=True,blank=True)
    # discount = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return str(self.user.username)


providers = [('facebook', 'Facebook'), ('google', 'Google'), ('twitter','Twitter')]
class SocialUsers(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    provider = models.CharField(max_length=8, choices=providers)
    socialID = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email

class MsgSubcourse(models.Model):
    subCourse = models.ForeignKey(SubCoursesModel,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=True)
    message = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title