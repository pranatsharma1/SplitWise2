#Serializers


from django.contrib.auth.models import User,Group
from rest_framework import serializers
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()



#User Creation Form

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
    



class OTPSerializer(serializers.ModelSerializer):
    """
    serializer for otp
    """

    class Meta:
        model = OTP
        fields = ['otp']


class LoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(
        required=True,
        style={'placeholder':'Username'}
    )

    class Meta:
        model=User
        fields=['username','password']
















































# #Wo jo django me forms hote the na....DRF me unhe hi Serializers kaha gaya hai


# from django.contrib.auth.models import User,Group
# from rest_framework import serializers
# from phonenumber_field.modelfields import PhoneNumberField
# from django.contrib.auth.hashers import make_password
# from .models import *
# from django.contrib.auth import get_user_model
# User = get_user_model()

# from rest_framework.exceptions import ValidationError
# from rest_framework.validators import UniqueValidator
# from rest_framework.validators import UniqueTogetherValidator


# from django.shortcuts import render
# from django.contrib.auth.models import User
# from rest_framework import viewsets
# from rest_framework.views import APIView
# from rest_framework.parsers import JSONParser
# from rest_framework.response import Response
# from quickstart.serializers import UserSerializer,LoginSerializer
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import serializers
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status,permissions
# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.views import ObtainAuthToken
# from .serializers import UserSerializer

# from django.contrib.auth import get_user_model
# User = get_user_model()

# # class RegisterUser(viewsets.ModelViewSet):
# #     queryset=User.objects.all().order_by('-date_joined')
# #     serializer_class = UserSerializer

# #     def get(self,request,format=None):
# #         users = User.objects.all()
# #         serializer = UserSerializer(users, many=True)
# #         return Response(serializer.data)

# #     def post(self, request, format=None):
# #         serializer = UserSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserSerializer(serializers.ModelSerializer):

#     username=serializers.CharField(
#         required=True,
#         style={'placeholder':'Username'}
#     )
#     first_name=serializers.CharField(
#         required=True,
#         style={'placeholder':'First Name'}
#     )
#     last_name=serializers.CharField(
#         required=True,
#         style={'placeholder':'Last Name'}
#     )
#     email=serializers.EmailField(
#         required=True,
#         style={'placeholder':'Email'}
#     )
#     phone_number=serializers.CharField(
#         required=True,
#         style={'placeholder':'Phone Number'}
#     )

#     class Meta:
#         model=User
#         fields=['url','username','first_name','last_name','email','phone_number','password']

#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data.get('password'))
#         return super(UserSerializer, self).create(validated_data)


# # class LoginRequest(ObtainAuthToken):
    
# #     serializer_class = LoginSerializer

# #     # def get(self,request,format=None):
# #     #     users = User.objects.all()
# #     #     serializer = LoginSerializer(users, many=True)
# #     #     return Response(serializer.data)

# #     def post(self, request, args,*kwargs):
# #         serializer = self.serializer_class(data=request.data,
# #                                            context={'request': request})
# #         serializer.is_valid(raise_exception=True)
# #         user = serializer.validated_data['user']
# #         token, created = Token.objects.get_or_create(user=user)
# #         return Response({
# #             'token': token.key,
# #             'user_id': user.pk,
# #             'email': user.email
# #         })
# #         # return Response(serializer.data, status=status.HTTP_201_CREATED)



# # #User Creation Form

# # class UserSerializer(serializers.ModelSerializer):
# #     """
# #     serializer for creating user object
# #     """
# #     email = serializers.EmailField(required=True,allow_blank=False,allow_null=False,
# #                                    validators=[UniqueValidator(queryset=User.objects.all(),
# #                                                                message="email already exists!",
# #                                                                lookup='exact')])
# #     username = serializers.CharField(required=True,allow_blank=False,allow_null=False,
# #                                      validators=[UniqueValidator(queryset=User.objects.all(),
# #                                                                  message="username is taken!,try another",
# #                                                                  lookup='exact')])
# #     password = serializers.CharField(style={'input_type': 'password'},required=True,
# #                                      allow_blank=False,allow_null=False)
# #     confirm_password = serializers.CharField(style={'input_type':'password'},required=True)

# #     class Meta:
# #         model = User
# #         fields = ('id','username', 'email','password','confirm_password')

# #     def validate(self, data):

# #         """
# #         function for password validation
# #         :param data:
# #         :return:
# #         """
# #         password = data.get('password')
# #         pass_cnf = data.get('confirm_password')

# #         if password != pass_cnf:
# #                raise ValidationError("Password didn't matched ")
# #         if len(password) < 6:
# #                raise ValidationError("password of minimum 6 digit is required")
# #         else:
# #             return data
     



# # class OTPSerializer(serializers.ModelSerializer):
# #     """
# #     serializer for otp
# #     """

# #     class Meta:
# #         model = OTP
# #         fields = ['otp']





# # class LoginSerializer(serializers.ModelSerializer):
# #     username=serializers.CharField(
# #         required=True,
# #         style={'placeholder':'Username'}
# #     )

# #     class Meta:
# #         model=User
# #         fields=['username','password']




























