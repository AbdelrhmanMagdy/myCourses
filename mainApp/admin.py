# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import UserProfileModel,CoursesModel,DatesModel,SubCourseImagesModel,CentreModel,SubCoursesModel,PromoCodeModel,BookingModel, studyCategoriesModel, PromoCodeUserModel, SocialUsers, MsgSubcourse

admin.site.register(UserProfileModel)
admin.site.register(CoursesModel)
admin.site.register(DatesModel)
admin.site.register(SubCourseImagesModel)
admin.site.register(CentreModel)
admin.site.register(SubCoursesModel)
admin.site.register(PromoCodeModel)
admin.site.register(BookingModel)
admin.site.register(studyCategoriesModel)
admin.site.register(PromoCodeUserModel)
admin.site.register(SocialUsers)
admin.site.register(MsgSubcourse)