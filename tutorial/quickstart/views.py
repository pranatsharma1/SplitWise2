from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from quickstart.serializers import SignUpSerializer,LoginSerializer,GroupSerializer,ExpenseSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import BasePermission, IsAuthenticated

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


#--------------------------------------------View for list of users-----------------------------------------------#

class ViewUser(viewsets.ModelViewSet):

    queryset=User.objects.all().order_by('-date_joined')      #Displaying objects in order of date joined
    serializer_class = UserSerializer                         

    def get(self,request,format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-------------------------------------------------------------------------------------------------------------#

#--------------------------------------Signup View to Create a New User----------------------------------------#

class SignUp(APIView):
    """
    List all user, or create a new user.
    """
    serializer_class = SignUpSerializer
  

    def post(self, request, *args, **kwargs):

        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        #fetching the data from serializer
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        first_name=serializer.validated_data['first_name']
        last_name=serializer.validated_data['last_name']
        phone_number=serializer.validated_data['phone_number']
        confirm_password=serializer.validated_data['confirm_password']

        #creating the user
        user = User.objects.create_user(username=username,email=email,password=password,confirm_password=confirm_password,first_name=first_name,last_name=last_name,phone_number=phone_number)

        # generating the otp and sending the email

        otp = randint(999, 10000)               #generating the 4 digit OTP
        data = OTP.objects.create(otp=otp,receiver=user)
        data.save()

        user.is_active = False                  # Abhi ke liye user ko inactive kar diya hai
        user.save()
        
        subject = 'Activate Your SplitItGo Account'
        message = render_to_string('account_activate.html', {
            'user': user,
            'OTP': otp,
        })
        from_mail = EMAIL_HOST_USER
        to_mail = [user.email]
        send_mail(subject, message, from_mail, to_mail, fail_silently=False)
        
        # subject = 'Activate Your SplitItGo Account'         # Email ka title hai ye
        # message = render_to_string
        # (   'account_activate.html',                        #  Template's name
        #   { 
        #     'user': user,                                   # details of user(jisko hum email bhej rahe hain) like username etc.
        #     'OTP': otp,                                     # OTP
        #   }
        # )
        
        # from_mail = EMAIL_HOST_USER                        # Wo email address jisse email send ho raha hai
        # to_mail = [user.email]                             # Wo email address jisko email send kar rhe hain

        # Sending the email now
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


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response=super(CustomAuthToken,self).post(request,*args,**kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'id': token.user_id,
        })

#-----------------------------------------------------------------------------------------------------------------#

#---------------------------------------View for creating a Group---------------------------------------------#

class GroupViewSet(APIView):

    permission_classes = [IsAuthenticated]                   #token-authentication
    serializer_class=GroupSerializer                  
    queryset=GroupModel.objects.all()

    def get(self,request,*args,**kwargs):
        user=self.request.user
        # print(user)
        group = GroupModel.objects.filter(users=user).order_by('-id')             #ordering the groups in descending order of id
        # print(group.group.id)
        serializer = GroupSerializer(group, many=True)

        # return Response({'details': serializer.data,
        #                         'group_id': group.id})
        # print(serializer.id)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
        group = GroupModel.objects.all()
        # print(group.id)
        serializer = GroupSerializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)

        name= serializer.validated_data['name']
        type=serializer.validated_data['type']
        list=serializer.validated_data['users']
        
        group=GroupModel.objects.all()
        if serializer.is_valid():
            temp=serializer.save()
            # print(group.id)
            print(temp.id)
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response({'details': 'Group has been successfully created',
                                'group_id': temp.id},status=status.HTTP_201_CREATED)
            # return Response(temp.id)                    
        return response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#----------------------------------------------------------------------------------------------------------------#


#-------------------------------------------View for creating an expense-----------------------------------------#

class ExpenseView(APIView):
    permission_classes = [IsAuthenticated]                   #token-authentication
    serializer_class=ExpenseSerializer
    queryset=Expense.objects.all()
    
    
    def get(self,request,group_id,format=None):
        user=self.request.user
        group=GroupModel.objects.get(id=group_id)
        
        expense1 = Expense.objects.filter(group_name__name=group.name).order_by('-id')            #ordering the objects in order of id
        expense2= Expense.objects.filter(group_name__users=user).order_by('-id')                  #ordering the objects in order of id
        expense=expense1 & expense2
        
        serializer = ExpenseSerializer(expense, many=True)
        
        return Response(serializer.data)

    def post(self,request,group_id,format=None):
        serializer = ExpenseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bill_name= serializer.validated_data['bill_name']
        description=serializer.validated_data['description']
        group_name= serializer.validated_data['group_name']
        amount= serializer.validated_data['amount']
        payer= serializer.validated_data['payer']
        # created_at=serializer.validated_data['created_at']
        if serializer.is_valid():
            temp=serializer.save()
            print(amount/temp.group_name.users.count())
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#------------------------------------------------------------------------------------------------------------------#



#---------------------------------------View for looking at an Expense---------------------------------------------#

class ExpenseViewSet(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class=ExpenseSerializer
    queryset=Expense.objects.all()
    
    def get(self,request,group_id,*args,**kwargs):
        
        user=self.request.user
        group=GroupModel.objects.get(id=group_id)
        
        # print(group)
        # expense_object=Expense.objects.all()
        expense1 = Expense.objects.filter(group_name__name=group.name).order_by('-id') # For descending
        expense2= Expense.objects.filter(group_name__users=user).order_by('-id')       #For Descending
        expense=expense1 & expense2
        
        # print(group_name)

        serializer = ExpenseSerializer(expense, many=True)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
        expense = Expense.objects.all()
        serializer = ExpenseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bill_name= serializer.validated_data['bill_name']
        description=serializer.validated_data['description']
        group_name= serializer.validated_data['group_name']
        amount= serializer.validated_data['amount']
        payer= serializer.validated_data['payer']

        if serializer.is_valid():
            temp=serializer.save()
            print(amount/temp.group_name.users.count())
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#----------------------------------------------------------------------------------------------------------------#









class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EditProfileSerializer

    def get_object(self):
        return self.request.user


class Pay(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class=PaySerializer

    def post(self,request,taker_id,*args,**kwargs):
        serializer = PaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        giver=serializer.validated_data['giver']
        taker=serializer.validated_data['taker']
        amount= serializer.validated_data['amount']


        # giver=request.user
        # taker=User.objects.get(id=taker_id)

        print("Giver = "+ giver.username)
        print("Taker = "+taker.username)
        print("Amount = "+str(amount))

        try:
            status1=Status.objects.get(giver=giver,taker=taker)
            print(status1)
        except Status.DoesNotExist:
            status1=Status.objects.create(giver=giver,taker=taker,amount=0)    

        status1.amount+=amount
        status1.save()
        print(status1)

        
        
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





class CurrentStatus(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,taker_id,*args,**kwargs):
        
        taker=User.objects.get(id=taker_id)
        user=request.user

        try:
            status1=Status.objects.get(giver=taker,taker=user)
            print(status1)
        except Status.DoesNotExist:
            status1=Status.objects.create(giver=taker,taker=user,amount=0)
        print(status1.amount)
        try:
            status2=Status.objects.get(giver=user,taker=taker)
            print(status2)
        except Status.DoesNotExist:
            status2=Status.objects.create(giver=user,taker=taker,amount=0)
        print(status2.amount)
        
        temp1=status1.amount-status2.amount
        temp2=status2.amount-status1.amount

        print("Amount given by "+status1.giver.username+" to "+status1.taker.username+" is "+str(temp1))
        print("Amount given by "+status2.giver.username+" to "+status2.taker.username+" is "+str(temp2))
       
        if (status1.amount-status2.amount>0):
            return Response({'message': 'You owe '+str(temp1) + ' to ' + status1.giver.username })

        elif (status1.amount-status2.amount<0):
            return Response({'message': 'You are owed ' +str(temp2) +' from '+status1.giver.username})

        else:
            return Response("All balances are settled up")

class AddFriend(APIView):
    
    permission_classes=[IsAuthenticated]
    serializer_class=FriendSerializer

    def get(self,request,*args,**kwargs):
        user=self.request.user
        print(user)
        friendlist=Friend.objects.get(friends=user)
        print(friendlist)

    def post(self,request,friend_id,*args,**kwargs):
        # user=self.request.user
        # print(user)
        friendlist=Friend.objects.get(user.id=self.request.user)
        print(friendlist)
        friendlist.friends.add(friend_id)

        return Response("User has been added to the friend list")














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








