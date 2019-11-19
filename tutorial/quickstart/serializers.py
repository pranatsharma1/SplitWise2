#Serializers


from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

#------------------------------------------------------------------------------------------------------------------------#
        
class UserSerializer(serializers.ModelSerializer):
    
    username=serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
        style={'placeholder':'Username'},
        validators=[UniqueValidator(queryset=User.objects.all(),
        message='This Username is already in use!',
        lookup='exact')]
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
        allow_blank=False,
        allow_null=False,
        style={'placeholder':'Email'},
        validators=[UniqueValidator(queryset=User.objects.all(),
        message='This Email is already in use!',
        lookup='exact')]
    )

    phone_number=serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
        style={'placeholder':'Phone Number'},
        validators=[UniqueValidator(queryset=User.objects.all(),
        message='This Phone Number is already in use!',
        lookup='exact')]
    )

    password = serializers.CharField(
        style={'input_type': 'password', 'placeholder':'Password'},
        required=True,
        allow_blank=False,
        allow_null=False)

    confirm_password = serializers.CharField(
        style={'input_type':'password','placeholder':'Confirm Password'},
        required=True)    
    
    class Meta:
        model=User
        fields=['url','username','first_name','last_name','email','phone_number','password','confirm_password']


#------------------------------------------------------------------------------------------------------------------------#


#------------------------------------------------------SignUp Form-------------------------------------------------------#

class SignUpSerializer(serializers.ModelSerializer):
    
    username=serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
        style={'placeholder':'Username'},
        validators=[UniqueValidator(queryset=User.objects.all(),
        message='This Username is already in use!',
        lookup='exact')]
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
        allow_blank=False,
        allow_null=False,
        style={'placeholder':'Email'},
        validators=[UniqueValidator(queryset=User.objects.all(),
        message='This Email is already in use!',
        lookup='exact')]
    )

    phone_number=serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
        style={'placeholder':'Phone Number'},
        validators=[UniqueValidator(queryset=User.objects.all(),
        message='This Phone Number is already in use!',
        lookup='exact')]
    )

    password = serializers.CharField(
        style={'input_type': 'password', 'placeholder':'Password'},
        required=True,
        allow_blank=False,
        allow_null=False)

    confirm_password = serializers.CharField(
        style={'input_type':'password','placeholder':'Confirm Password'},
        required=True)    
    
    class Meta:
        model=User
        fields=['url','username','first_name','last_name','email','phone_number','password','confirm_password']
    
    def validate_phone_number(self,phone_number):

        if len(phone_number)>10:
            raise serializers.ValidationError("Please enter a valid Phone number")
        elif len(phone_number)<10:
            raise serializers.ValidationError("Please enter a valid Phone number")
        elif phone_number.isdigit():
            return phone_number
        else:    
            raise serializers.ValidationError("Please enter a valid Phone number")
    def validate(self,email):
        try:
            match= User.objects.get(email=email)
        except User.DoesNotExist:
            return data
        
        raise serializers.ValidationError('This email is already in use')    
    def validate(self, data):

        """
        function for password validation
        :param data:
        :return:
        """
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
               raise serializers.ValidationError("Password didn't matched ")
        if len(password) < 6:
               raise serializers.ValidationError("Password of minimum 6 digits is required")
        else:
            return data
    
#------------------------------------------------------------------------------------------------------------------------#


#--------------------------------------------------Serializer for OTP----------------------------------------------------#
class OTPSerializer(serializers.ModelSerializer):
    """
    serializer for otp
    """

    class Meta:
        model = OTP
        fields = ['otp']

#------------------------------------------------------------------------------------------------------------------------#


#-------------------------------------------------Serializer for Login---------------------------------------------------#
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


#------------------------------------------------------------------------------------------------------------------------#


#--------------------------------------------Serializer for Creating a Group--------------------------------------------#

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model=GroupModel
        # fields=['id','name','admin','users','type']
        fields='__all__'
        read_only_fields = ('id','created_at')
#------------------------------------------------------------------------------------------------------------------------#


#---------------------------------------------Serializer for Adding Expense----------------------------------------------#

class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model=Expense
        # fields=['bill_name','description','group_name','amount','payer',]        
        fields='__all__'

#------------------------------------------------------------------------------------------------------------------------#


#-------------------------------------------------Edit Profile Form------------------------------------------------------#

class EditProfileSerializer(serializers.ModelSerializer):
    
    username=serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
        style={'placeholder':'Username'},
        validators=[UniqueValidator(queryset=User.objects.all(),
        message='This Username is already in use!',
        lookup='exact')]
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
        allow_blank=False,
        allow_null=False,
        style={'placeholder':'Email'},
        validators=[UniqueValidator(queryset=User.objects.all(),
        message='This Email is already in use!',
        lookup='exact')]
    )

    phone_number=serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
        style={'placeholder':'Phone Number'},
        validators=[UniqueValidator(queryset=User.objects.all(),
        message='This Phone Number is already in use!',
        lookup='exact')]
    )

    password = serializers.CharField(
        style={'input_type': 'password', 'placeholder':'Password'},
        required=True,
        allow_blank=False,
        allow_null=False)

    confirm_password = serializers.CharField(
        style={'input_type':'password','placeholder':'Confirm Password'},
        required=True)    
    
    class Meta:
        model=User
        fields=['url','username','first_name','last_name','email','phone_number','password','confirm_password']
    
    def validate_phone_number(self,phone_number):

        if len(phone_number)>10:
            raise serializers.ValidationError("Please enter a valid Phone number")
        elif len(phone_number)<10:
            raise serializers.ValidationError("Please enter a valid Phone number")
        elif phone_number.isdigit():
            return phone_number
        else:    
            raise serializers.ValidationError("Please enter a valid Phone number")
    def validate(self,email):
        try:
            match= User.objects.get(email=email)
        except User.DoesNotExist:
            return data
        
        raise serializers.ValidationError('This email is already in use')    
    def validate(self, data):

        """
        function for password validation
        :param data:
        :return:
        """
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
               raise serializers.ValidationError("Password didn't matched ")
        if len(password) < 6:
               raise serializers.ValidationError("Password of minimum 6 digits is required")
        else:
            return data
    
#------------------------------------------------------------------------------------------------------------------------#


#-----------------------------------------Serializer for One to One Payment----------------------------------------------#


class PaySerializer(serializers.ModelSerializer):

    class Meta:
        model=Status
        fields=['taker','giver','amount']   

#------------------------------------------------------------------------------------------------------------------------#


#-------------------------------------Serializer for Adding Friend to the Friendlist-------------------------------------#

# class FriendSerializer(serializers.ModelSerializer):

#     class Meta:
#         model=Friend
#         fields='__all__'

#------------------------------------------------------------------------------------------------------------------------#        