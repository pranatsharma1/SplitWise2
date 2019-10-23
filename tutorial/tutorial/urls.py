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
from rest_framework_jwt.views import obtain_jwt_token
from django.contrib.auth import get_user_model
from quickstart.views import LoginRequest
User = get_user_model()


router=routers.DefaultRouter()
router.register(r'users',views.RegisterUser)
# router.register(r'groups',views.GroupViewSet)
# router.register(r'login',views.LoginRequest)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('token-auth/', obtain_jwt_token),
    url(r'login/',LoginRequest.as_view()),
    url(r'', include(('rest_pyotp.routers','pyotp'), namespace='rest-pyotp-urls')),
    url(r'signup/',views.SignUp.as_view()),
]
