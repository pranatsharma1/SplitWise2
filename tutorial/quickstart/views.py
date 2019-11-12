from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from quickstart.serializers import SignUpSerializer,LoginSerializer,GroupSerializer,ExpenseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .permissions import *
from django.db.models import Q
from .backends import EmailOrUsername

import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status,filters
from rest_framework import generics,viewsets,mixins
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.core.mail import send_mail
from tutorial.settings import EMAIL_HOST_USER
from django.contrib.auth import login,logout
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import action

from .serializers import *
from .models import OTP
from random import *
from django.contrib.auth import get_user_model
User = get_user_model()

#--------------------------------------Signup View to Create a New User----------------------------------------#

class SignUp(APIView):
    """
    List all user, or create a new user.
    """
    serializer_class = SignUpSerializer
  

    def post(self, request, *args, **kwargs):

        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        first_name=serializer.validated_data['first_name']
        last_name=serializer.validated_data['last_name']
        phone_number=serializer.validated_data['phone_number']
        confirm_password=serializer.validated_data['confirm_password']
        user = User.objects.create_user(username=username,email=email,password=password,confirm_password=confirm_password,first_name=first_name,last_name=last_name,phone_number=phone_number)

        otp = randint(999, 10000)
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
        return Response({'details': username+',Please verify your OTP sent to your Email-id to complete registration.',
                                'user_id': user.id })

#-----------------------------------------------------------------------------------------------------------------#

#-----------------------------------View for verifying the OTP sent to the user-------------------------------#

class ValidateOtp(APIView):
   
    serializer_class = OTPSerializer
    permission_classes = (permissions.AllowAny,IsNotActive)
    authentication_classes = (TokenAuthentication,)

    def post(self,request,user_id,*args,**kwargs):
        code = OTPSerializer(data=request.data)
        code.is_valid(raise_exception=True)
        code = code.validated_data['otp']
        try:
            otp = OTP.objects.get(receiver=user_id)
        except(TypeError, ValueError, OverflowError, OTP.DoesNotExist):
                otp = None
        try:
            receiver = User.objects.get(id=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            receiver = None
        if otp is None:
            return Response({'error':'you are not a valid user'},status=status.HTTP_400_BAD_REQUEST)

        elif timezone.now() - otp.sent_on >= timedelta(days=0,hours=0,minutes=5,seconds=0):
            otp.delete()
            return Response({'detail':'OTP expired!',
                                 'user_id':user_id})

        if otp.otp == code:
            receiver.is_active = True
            receiver.save()
           
            otp.delete()
            return Response({'message': 'Thank you for Email Verification. You can Login to your account now'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message':'Invalid OTP',},status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

#----------------------------------------------------------------------------------------------------------------#

#------------------------------------------View for Resending the OTP--------------------------------------------#

class ResendOtp(generics.CreateAPIView):
   
    serializer_class = OTPSerializer
    permission_classes = (permissions.AllowAny,IsNotActive)
    authentication_classes = (TokenAuthentication,)

    def get(self,request,user_id,*args,**kwargs):
        try:
            user = User.objects.get(id=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is None:
            return Response({'error':'Not a valid user!'})
        otp = OTP.objects.filter(receiver=user)
        if otp:
            otp.delete()
        otp = randint(100000, 1000000)
        data = OTP.objects.create(otp=otp,receiver= user)
        data.save()
        subject = 'Activate Your SplitItGo Account'
        message = render_to_string('account_activate.html', {
            'user': user,
            'OTP': otp,
        })
        from_mail = EMAIL_HOST_USER
        to_mail = [user.email]
        send_mail(subject, message, from_mail, to_mail, fail_silently=False)
        return Response({'details': user.username +',Please verify your OTP sent to your Email-id to complete registration.',
                         'user_id': user_id },
                        status=status.HTTP_201_CREATED)

#----------------------------------------------------------------------------------------------------------------#

#---------------------------------------View for Login the User--------------------------------------------------#

class LoginRequest(APIView):
    """
    the user can login either with email or username. EmailOrUsername is the function for it.
    """

    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self,request,*args,**kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uname_or_em = serializer.validated_data['uname_or_em']
        password = serializer.validated_data['password']
        user = EmailOrUsername(self,uname_or_em = uname_or_em,password=password)

        if user == 2:
            return Response({'error':'Invalid Username or Email!!'},
                                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        elif user == 3:
            return Response({'error':'Incorrect Password'},
                                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            if user.is_active:
                login(request, user)
                return Response({'detail':'successfully Logged in!','user_id': user.id,
                                 'username':user.username},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error':'Please! varify Your Email First','user_id':user.id},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)


#------------------------------------------View for logging the user out----------------------------------------#

class Logout(APIView):
    """
    logout view.Only authenticated user can access this url(by default)
    """
    def get(self,request,*args,**kwargs):
        logout(request)
        return Response({'message':'successfully logged out'},
                        status=status.HTTP_200_OK)


# class CustomAuthToken(ObtainAuthToken):

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })

#-----------------------------------------------------------------------------------------------------------------#

#--------------------------------------------View for list of users-----------------------------------------------#

class ViewUser(viewsets.ModelViewSet):
    queryset=User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get(self,request,format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # serializer = UserSerializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-------------------------------------------------------------------------------------------------------------#

#---------------------------------------View for creating a Group---------------------------------------------#

class GroupViewSet(APIView):
    serializer_class=GroupSerializer
    queryset=GroupModel.objects.all()

    def get(self,request,user_id,*args,**kwargs):
        user=User.objects.get(id=user_id)
        group = GroupModel.objects.filter(users=user)
        serializer = GroupSerializer(group, many=True)
        return Response(serializer.data)

    def post(self,request,user_id,*args,**kwargs):
        group = GroupModel.objects.all()
        serializer = GroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name= serializer.validated_data['name']
        type=serializer.validated_data['type']
        list=serializer.validated_data['users']
        print(list)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#----------------------------------------------------------------------------------------------------------------#


#-------------------------------------------View for creating an expense-----------------------------------------#

class ExpenseView(APIView):
    serializer_class=ExpenseSerializer
    queryset=Expense.objects.all()

    def get(self,request,user_id,group_id,format=None):
        expense = Expense.objects.all()
        serializer = GroupSerializer(expense, many=True)
        return Response(serializer.data)

    def post(self,request,user_id,group_id,format=None):
        serializer = ExpenseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bill_name= serializer.validated_data['bill_name']
        description=serializer.validated_data['description']
        group_name= serializer.validated_data['group_name']
        amount= serializer.validated_data['amount']
        payer= serializer.validated_data['payer']
        # created_at=serializer.validated_data['created_at']
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






#---------------------------------------View for looking at an Expense---------------------------------------------#

class ExpenseViewSet(APIView):
    serializer_class=ExpenseSerializer
    queryset=Expense.objects.all()
    
    def get(self,request,user_id,group_id,*args,**kwargs):
        
        user=User.objects.get(id=user_id)
        group=GroupModel.objects.get(id=group_id)
        
        print(group)
        # expense_object=Expense.objects.all()
        expense1 = Expense.objects.filter(group_name__name=group.name)
        expense2= Expense.objects.filter(group_name__users=user)
        expense=expense1 & expense2
        
        # print(group_name)

        serializer = ExpenseSerializer(expense, many=True)
        return Response(serializer.data)

    def post(self,request,user_id,*args,**kwargs):
        expense = Expense.objects.all()
        serializer = ExpenseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bill_name= serializer.validated_data['bill_name']
        description=serializer.validated_data['description']
        group_name= serializer.validated_data['group_name']
        amount= serializer.validated_data['amount']
        payer= serializer.validated_data['payer']

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#----------------------------------------------------------------------------------------------------------------#



































# class Login(APIView):
    
#     serializer_class = LoginSerializer
#     authentication_classes = (TokenAuthentication,)

#     # def get(self,request,format=None):
#     #     users = User.objects.all()
#     #     serializer = LoginSerializer(users, many=True)
#     #     return Response(serializer.data)

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['uname_or_em']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })
#         # return Response(serializer.data, status=status.HTTP_201_CREATED)









