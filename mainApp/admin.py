# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import CertificatesModel,UserProfileModel,CoursesModel,DatesModel,SubCourseImagesModel,CentreModel,SubCoursesModel,PromoCodeModel,BookingModel, studyCategoriesModel

admin.site.register(CertificatesModel)
admin.site.register(UserProfileModel)
admin.site.register(CoursesModel)
admin.site.register(DatesModel)
admin.site.register(SubCourseImagesModel)
admin.site.register(CentreModel)
admin.site.register(SubCoursesModel)
admin.site.register(PromoCodeModel)
admin.site.register(BookingModel)
admin.site.register(studyCategoriesModel)