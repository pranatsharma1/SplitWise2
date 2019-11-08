#Serializers


from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

        

#--------------------------------------------------SignUp Form--------------------------------------------------#

class SignUpSerializer(serializers.ModelSerializer):
    
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
    
    def validate(self,data):
        email=data.get('email')

        try:
            match= User.objects.get(email=email)
        except User.DoesNotExist:
            return data
        
        raise serializers.ValidationError('This email is already in use')
    
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
    serializer for login
    """

    uname_or_em = serializers.CharField(allow_null=False,required=True)
    password = serializers.CharField(style={'input_type': 'password'},required=True,
                                     allow_blank=False,allow_null=False)

    class Meta:
        model = User
        fields = ('uname_or_em','password')

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model=GroupModel
        fields=['name','users','type']