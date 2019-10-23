from rest_framework import permissions
from .models import *


class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        user=User.objects.filter(user=self.request.user)
        if user and user.is_active==False:
            return True
        else:
            return False


class IsNotActive(permissions.BasePermission):
    """
    checking if user is already active or not.
    """
    def has_permission(self, request, view):
        if request.user.is_active == True:
             return False
        return True


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,

        # Write permissions are only allowed to the owner of the address.
        return obj.user.username == request.user.username


class IsBuyer(permissions.BasePermission):
    """
  Custom permission to only allow buyers to have access.
  """
    def has_permission(self, request, view):
        user =request.user
        roles = user.roles.all()
        for role in roles:
            if role.role == 'Buyer':
                return True
        return False


class IsSeller(permissions.BasePermission):
    """
 Custom permission to only allow sellers to have access.
 """

    def has_permission(self, request, view):
        user =request.user
        role = user.roles.filter(role='Seller')
        if role:
            return True
        else:
            return False


class IsAdmin(permissions.BasePermission):
    """
 Custom permission to only allow admin to create Role
 """

    def has_permission(self, request, view,):
        user = request.user
        if user.is_staff== True:
            return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user.username == request.user.username


class IsSellerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list','retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            user =request.user
            role = user.roles.filter(role='Seller')
            if role:
                return True
            else:
                return False