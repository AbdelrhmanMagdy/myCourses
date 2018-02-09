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
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    mobile = models.CharField(max_length=11)
    fieldOfStudy = models.ManyToManyField(studyCategoriesModel,blank=True,related_name='userCategories') 
    certificate = models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
        return str(self.user)

# class CertificatesModel(models.Model):
    # certificate = models.FileField(upload_to='media/certificates', blank=True,null=True)
    # user = models.ForeignKey(UserProfileModel,on_delete=models.CASCADE, null=True)

class CoursesModel(models.Model):
    courseName = models.CharField(max_length=50)
    courseImage = models.ImageField(upload_to='media/images', blank=True,null=True)
    courseSlogun = models.CharField(max_length=250)
    categories = models.ManyToManyField(studyCategoriesModel,blank=True,related_name='courseCategories') 

    def __str__(self):
        return str(self.courseName)


class CentreModel(models.Model):
    centreName = models.CharField(max_length=50)
    lat = models.DecimalField(max_digits=100, decimal_places=6)
    lon = models.DecimalField(max_digits=100, decimal_places=6)
    address = models.CharField(max_length=100)
    info = models.CharField(max_length=500)
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE, db_index=True,blank=True)
    image = models.ImageField(upload_to='media/images', blank=True,null=True)
    def __str__(self):
        return str(self.centreName)
class SubCoursesModel(models.Model):
    instructorName = models.CharField(max_length=50)
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
    images = models.ImageField(upload_to='media/images', blank=True,null=True)
    subCourse = models.ForeignKey(SubCoursesModel, on_delete=models.CASCADE,null=True,blank=True, related_name='images')
    
    def __str__(self):
        return str(self.subCourse.instructorName)

class PromoCodeModel(models.Model):
    promoCode = models.CharField(max_length=50)
    discount = models.IntegerField()
    def __str__(self):
        return str(self.promoCode)
class BookingModel(models.Model):
    user = models.ForeignKey(UserProfileModel ,on_delete=models.CASCADE)
    promoCode = models.ForeignKey(PromoCodeModel, null=True,blank=True,on_delete=models.CASCADE)
    subCourse = models.ForeignKey(SubCoursesModel,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user.user.username)