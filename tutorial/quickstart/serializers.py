#Serializers


from django.contrib.auth.models import User,Group
from rest_framework import serializers
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()



#--------------------------------------------------SignUp Form--------------------------------------------------#

class UserSerializer(serializers.ModelSerializer):

    username=serializers.CharField(
        required=True,
        style={'placeholder':'Username'}
    )
    first_name=serializers.CharField(
        required=True,
        style={'placeholder':'First Name'}
    )
    last_name=serializers.CharField(
        required=True,
        style={'placeholder':'Last Name'}
    )
    email=serializers.EmailField(
        required=True,
        style={'placeholder':'Email'}
    )
    phone_number=serializers.CharField(
        required=True,
        style={'placeholder':'Phone Number'}
    )

    class Meta:
        model=User
        fields=['url','username','first_name','last_name','email','phone_number','password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
    
#----------------------------------------------------------------------------------------------------------------#

#--------------------------------------------------Serializer for OTP--------------------------------------------#
class OTPSerializer(serializers.ModelSerializer):
    """
    serializer for otp
    """

    class Meta:
        model = OTP
        fields = ['otp']

class LoginSerializer(serializers.ModelSerializer):
    """
    login serializer
    """

    uname_or_em = serializers.CharField(allow_null=False,required=True)
    password = serializers.CharField(style={'input_type': 'password'},required=True,
                                     allow_blank=False,allow_null=False)

    class Meta:
        model = User
        fields = ('uname_or_em','password')

