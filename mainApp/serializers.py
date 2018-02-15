from rest_framework import serializers
from .models import UserProfileModel
from django.contrib.auth.models import User
from .models import UserProfileModel,CoursesModel,DatesModel,SubCourseImagesModel,CentreModel,SubCoursesModel,PromoCodeModel,BookingModel, studyCategoriesModel, PromoCodeUserModel, SocialUsers

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension
class SubCourseImagesSerializer(serializers.ModelSerializer):
    images = Base64ImageField(max_length=None, use_url=True,)
    class Meta:
        model =  SubCourseImagesModel
        exclude = ('id',)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =  studyCategoriesModel
        exclude = ('')


# class CertificatesImageSerializer(serializers.ModelSerializer):
#     certificates = Base64ImageField(max_length=None, use_url=True,)
#     class Meta:
#         model = CertificatesModel
#         exclude = ('')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username','is_staff','first_name','is_superuser')
class UserProfileSerializer(serializers.ModelSerializer):
    # fieldOfStudy = CategorySerializer(many=True,required=False)
    # user = UserSerializer()
    image = Base64ImageField(max_length=None, use_url=True,required=False)
    class Meta:
        model = UserProfileModel
        exclude = ('id',)


class CoursesSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True,required=False)   
    courseImage =  Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model = CoursesModel
        exclude = ('')
class CentreSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True,required=False)
    class Meta:
        model = CentreModel
        exclude = ('')
class StartingDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatesModel
        exclude = ('')
class CoursesSpecificSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursesModel
        exclude = ('courseImage','courseSlogun','categories')
class SubCourseSerializer(serializers.ModelSerializer):
    dates = StartingDateSerializer(many=True)
    images = SubCourseImagesSerializer(many=True)
    course = CoursesSpecificSerializer()
    
    # centre = CentreSerializer()
    class Meta:
        model =  SubCoursesModel
        exclude = ('')

class SubCoursePostSerializer(serializers.ModelSerializer):    
    dates = StartingDateSerializer(many=True,required=False)
    images = SubCourseImagesSerializer(many=True,required=False)
    class Meta:
        model =  SubCoursesModel
        exclude = ('')
class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCodeModel
        exclude = ('id',)
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingModel
        exclude = ('')
class UserBookingSerializer(serializers.ModelSerializer):
    promoCode = PromoCodeSerializer()
    subCourse = SubCourseSerializer()
    class Meta:
        model = BookingModel
        exclude = ('id','user')
class BookingSubCourseSerializer(serializers.ModelSerializer):
    dates = StartingDateSerializer(many=True)
    course = CoursesSpecificSerializer()
    class Meta:
        model =  SubCoursesModel
        exclude = ('id','rate','fees','is_trend','centre')
class BookingUserSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = User
        exclude = ('last_login','password','is_superuser','username','last_name','is_staff','is_active','date_joined','groups','user_permissions',)

class BookingFinalSerializer(serializers.ModelSerializer):
    user = BookingUserSerializer()
    subCourse = BookingSubCourseSerializer()
    promoCode = PromoCodeSerializer()
    class Meta:
        model = BookingModel
        exclude = ('id',)

class PromoCodeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCodeUserModel
        exclude = ('')




class SocialSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialUsers
        fields = ('provider','socialID')


class SocialUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email','first_name')
