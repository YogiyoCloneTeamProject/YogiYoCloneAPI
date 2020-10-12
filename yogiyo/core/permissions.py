from rest_framework import permissions

from orders.models import Order


class IsOrderOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        """order의 owner == request.user """
        return request.user == Order.objects.get(id=view.kwargs.get('order_pk')).owner


class IsUserSelf(permissions.IsAuthenticated):
    """유저 자신에 대한 권한"""

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsOwner(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        """super_user permission"""
        return request.user and request.user.is_authenticated and request.user.is_superuser
