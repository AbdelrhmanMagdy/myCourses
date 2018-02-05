# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

educationOptions = [('university','university'),('highSchool','highSchool'),('school','school')]

# Create your models here.

class CertificatesModel(models.Model):
    certificate = models.FileField(upload_to='Certificates', blank=True,null=True)


class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    mobile = models.CharField(max_length=11)
    educationLevel = models.CharField(max_length=15, choices=educationOptions)
    university = models.CharField(max_length=15,blank=True) 
    faculty = models.CharField(max_length=15, blank=True) # faculty if exist and it's major / minor
    major = models.CharField(max_length=15,blank=True) # 3elmy / adby 
    certificates = models.ForeignKey(CertificatesModel,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.user)

class CoursesModel(models.Model):
    courseName = models.CharField(max_length=50)
    courseImage = models.ImageField(upload_to='Images', blank=True,null=True)
    courseSlogun = models.CharField(max_length=250)

    def __str__(self):
        return str(self.courseName)

class DatesModel(models.Model):
    date = models.DateField()
    def __str__(self):
        return str(self.date)

class CentreImagesModel(models.Model):
    images = models.ImageField(upload_to='Images', blank=True,null=True)

class CentreModel(models.Model):
    centreName = models.CharField(max_length=50)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=100)
    info = models.CharField(max_length=500)
    centreImages = models.ForeignKey(CentreImagesModel, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return str(self.centreName)

class SubCoursesModel(models.Model):
    centre = models.ForeignKey(CentreModel, on_delete=models.CASCADE,null=True,blank=True)
    instructorName = models.CharField(max_length=50)
    startingDate = models.ForeignKey(DatesModel, on_delete=models.CASCADE,null=True,blank=True)
    rate =  models.IntegerField()
    fees = models.CharField(max_length=50)
    subCourseImage = models.ImageField(upload_to='Images', blank=True,null=True)
    # trend

    def __str__(self):
        return str(self.centre.centreName)

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