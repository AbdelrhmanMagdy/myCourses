# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import CertificatesModel,UserProfileModel,CoursesModel,DatesModel,CentreImagesModel,CentreModel,SubCoursesModel,PromoCodeModel,BookingModel

admin.site.register(CertificatesModel)
admin.site.register(UserProfileModel)
admin.site.register(CoursesModel)
admin.site.register(DatesModel)
admin.site.register(CentreImagesModel)
admin.site.register(CentreModel)
admin.site.register(SubCoursesModel)
admin.site.register(PromoCodeModel)
admin.site.register(BookingModel)