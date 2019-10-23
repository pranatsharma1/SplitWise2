from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from quickstart.serializers import UserSerializer,LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserSerializer
from .models import OTP
from random import *
from django.contrib.auth import get_user_model
User = get_user_model()



from .serializers import *
from .permissions import *
from django.db.models import Q
from .backends import EmailOrUsername
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User=get_user_model()
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status,filters
from rest_framework import generics,viewsets,mixins
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.core.mail import send_mail
from tutorial.settings import EMAIL_HOST_USER
from random import *
from rest_framework import permissions
from .models import OTP
from django.contrib.auth import login,logout
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import action



class SignUp(APIView):
    """
    List all user, or create a new user.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        first_name=serializer.validated_data['first_name']
        last_name=serializer.validated_data['last_name']
        phone_number=serializer.validated_data['phone_number']

        user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name,phone_number=phone_number)
        otp = randint(100000, 1000000)
        data = OTP.objects.create(otp=otp,receiver=user)
        data.save()
        user.is_active = False
        user.save()
        subject = 'Activate Your SplitItGo Account'
        message = render_to_string('account_activate.html', {
            'user': user,
            'OTP': otp,
         })
        from_mail = EMAIL_HOST_USER
        to_mail = [user.email]
        send_mail(subject, message, from_mail, to_mail, fail_silently=False)
        return Response({'details': username+',Please confirm your email to complete registration.',
                                'user_id': user.id })



class RegisterUser(viewsets.ModelViewSet):
    queryset=User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get(self,request,format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginRequest(ObtainAuthToken):
    
    serializer_class = LoginSerializer

    # def get(self,request,format=None):
    #     users = User.objects.all()
    #     serializer = LoginSerializer(users, many=True)
    #     return Response(serializer.data)

    def post(self, request, args,*kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        # return Response(serializer.data, status=status.HTTP_201_CREATED)



























































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




# from django.shortcuts import render


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset=User.objects.all().order_by('-date_joined')
#     serializer_class= UserSerializer


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


# # class LoginRequest(ObtainAuthToken):
    
# #     serializer_class = LoginSerializer

# #     def get(self,request,format=None):
# #         users = User.objects.all()
# #         serializer = LoginSerializer(users, many=True)
# #         return Response(serializer.data)

# #     def post(self, request, *args,**kwargs):
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
# #         return Response(serializer.data, status=status.HTTP_201_CREATED)


# # class GroupViewSet(viewsets.ModelViewSet):
# #     """
# #     API endpoint that allows groups to be viewed or edited.
# #     """    
# #     queryset=Group.objects.all()
# #     serializer_class=GroupSerializer


# from .serializers import *
# from .permissions import *
# from django.db.models import Q
# from .backends import EmailOrUsername
# from rest_framework.response import Response
# from django.contrib.auth import get_user_model
# User=get_user_model()
# import django_filters.rest_framework
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import status,filters
# from rest_framework import generics,viewsets,mixins
# from rest_framework.views import APIView
# from django.template.loader import render_to_string
# from django.core.mail import send_mail
# from quickstart.settings import EMAIL_HOST_USER
# from random import *
# from rest_framework import permissions
# from .models import OTP
# from django.contrib.auth import login,logout
# from django.utils import timezone
# from datetime import timedelta
# from rest_framework.decorators import action



# # class SignUp(APIView):
# #     """
# #     List all user, or create a new user.
# #     """
# #     serializer_class = UserSerializer
# #     permission_classes = (permissions.AllowAny,)

# #     def post(self, request, *args, **kwargs):
# #         serializer = UserSerializer(data=request.data)
# #         serializer.is_valid(raise_exception=True)
# #         email = serializer.validated_data['email']
# #         username = serializer.validated_data['username']
# #         password = serializer.validated_data['password']
# #         user = User.objects.create_user(username=username,email=email,password=password)
# #         otp = randint(100000, 1000000)
# #         data = OTP.objects.create(otp=otp,receiver=user)
# #         data.save()
# #         user.is_active = False
# #         user.save()
# #         subject = 'Activate Your Dealmart Account'
# #         message = render_to_string('account_activate.html', {
# #             'user': user,
# #             'OTP': otp,
# #          })
# #         from_mail = EMAIL_HOST_USER
# #         to_mail = [user.email]
# #         send_mail(subject, message, from_mail, to_mail, fail_silently=False)
# #         return Response({'details': username+',Please confirm your email to complete registration.',
# #                                 'user_id': user.id })


# # class Activate(APIView):
# #     """
# #     Activate verifies the stored otp and the otp entered by user.
# #     """
# #     permission_classes = (permissions.AllowAny,IsNotActive)
# #     serializer_class = OTPSerializer

# #     def post(self,request,user_id,*args,**kwargs):
# #         code = OTPSerializer(data=request.data)
# #         code.is_valid(raise_exception=True)
# #         code = code.validated_data['otp']
# #         try:
# #             otp = OTP.objects.get(receiver=user_id)
# #         except(TypeError, ValueError, OverflowError, OTP.DoesNotExist):
# #                 otp = None
# #         try:
# #             receiver = User.objects.get(id=user_id)
# #         except(TypeError, ValueError, OverflowError, User.DoesNotExist):
# #             receiver = None
# #         if otp is None or receiver is None:
# #             return Response({'error':'you are not a valid user'},status=status.HTTP_400_BAD_REQUEST)

# #         elif timezone.now() - otp.sent_on >= timedelta(days=0,hours=0,minutes=2,seconds=0):
# #             otp.delete()
# #             return Response({'detail':'OTP expired!',
# #                                  'user_id':user_id})

# #         if otp.otp == code:
# #             receiver.is_active = True
# #             receiver.save()
# #             buyer = Role.objects.get(role='Buyer')
# #             receiver.roles.add(buyer)
# #             # Cart.objects.create(user=receiver)
# #             # login(request, receiver)
# #             otp.delete()
# #             return Response({'message': 'Thank you for Email Verification you are successfully logged in'},
# #                             status=status.HTTP_200_OK)
# #         else:
# #             return Response({'error':'Invalid OTP',},status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


# # class ResendOtp(generics.CreateAPIView):
# #     """
# #     views for resend the otp.
# #     """
# #     serializer_class = OTPSerializer
# #     permission_classes = (permissions.AllowAny,IsNotActive)

# #     def get(self,request,user_id,*args,**kwargs):
# #         try:
# #             user = User.objects.get(id=user_id)
# #         except(TypeError, ValueError, OverflowError, User.DoesNotExist):
# #             user = None
# #         if user is None:
# #             return Response({'error':'Not a valid user!'})
# #         otp = OTP.objects.filter(receiver=user)
# #         if otp:
# #             otp.delete()
# #         otp = randint(100000, 1000000)
# #         data = OTP.objects.create(otp=otp,receiver= user)
# #         data.save()
# #         subject = 'Activate Your Dealmart Account'
# #         message = render_to_string('account_activate.html', {
# #             'user': user,
# #             'OTP': otp,
# #         })
# #         from_mail = EMAIL_HOST_USER
# #         to_mail = [user.email]
# #         send_mail(subject, message, from_mail, to_mail, fail_silently=False)
# #         return Response({'details': user.username +',Please confirm your email to complete registration.',
# #                          'user_id': user_id },
# #                         status=status.HTTP_201_CREATED)
































# # # Create your views here.
# # from django.contrib.auth.models import User,Group
# # from rest_framework import viewsets
# # from quickstart.serializers import UserSerializer,GroupSerializer

# # from django.contrib.auth import get_user_model
# # User = get_user_model()
