"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from rest_framework import routers
from quickstart import views
from django.conf.urls import url
# from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token,verify_jwt_token
from django.contrib.auth import get_user_model
from quickstart.views import LoginRequest
User = get_user_model()


router=routers.DefaultRouter()
router.register(r'users',views.ViewUser)
# router.register(r'Groups',views.GroupViewSet,basename='Groups')
# router.register(r'groups',views.GroupViewSet)
# router.register(r'login',views.LoginRequest)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('login/', obtain_jwt_token),
    path('custom-login/',views.CustomAuthToken.as_view()),
    path('loginrequest/',views.LoginRequest.as_view()),
    path('logout/',views.LoginRequest.as_view()),
    path('token-refresh/', refresh_jwt_token),
    path('token-verify/', verify_jwt_token),
    url(r'^signup/$', views.SignUp.as_view()),
    url(r'^validate/(?P<user_id>[0-9]+)/$', views.ValidateOtp.as_view(), name='validate-otp'),
    url(r'^resendotp/(?P<user_id>[0-9]+)/$',views.ResendOtp.as_view(), name='resend-otp'),
    url(r'^profile/create-group/$',views.GroupViewSet.as_view(),name='Group'),
    url(r'^profile/groups/(?P<group_id>[0-9]+)/create-expense/$',views.ExpenseView.as_view(),name='Expense'),
    url(r'^profile/groups/$',views.GroupViewSet.as_view(),name='Group'),
    url(r'^profile/groups/(?P<group_id>[0-9]+)/expenses/$',views.ExpenseViewSet.as_view(),name='Expenses'),
    url(r'^profile/edit_profile/$',views.ManageUserView.as_view(),name='edit_profile'),
    url(r'^profile/(?P<taker_id>[0-9]+)/pay/$',views.Pay.as_view(),name='pay'),
    url(r'^profile/friendlist/$',views.AddFriend.as_view(),name='FriendList'),
    url(r'^profile/add_friend/(?P<friend_id>[0-9]+)/$',views.AddFriend.as_view(),name='AddFriend'),
    url(r'profile/current_status/(?P<taker_id>[0-9]+)/',views.CurrentStatus.as_view(),name='Current_Status'),
    url(r'^profile/get_username/(?P<user_id>[0-9]+)/',views.GetUsername.as_view(),name='Get_Username'),
    url(r'^profile/get_email/(?P<user_id>[0-9]+)/',views.GetEmail.as_view(),name='Get_Email')
]




