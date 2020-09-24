from rest_framework import permissions

from orders.models import Order


class ReviewIsOwner(permissions.BasePermission):
    """
    delete : is_owner
    create : is_authenticated , is_owner
    """

    def has_permission(self, request, view):
        """review에 order의 owner == request.user """
        return request.user and request.user.is_authenticated and request.user == Order.objects.get(id=view.kwargs['order_pk']).owner

    def has_object_permission(self, request, view, obj):
        if request.method == 'delete':
            return obj.owner == request.user
        return request.user and request.user.is_authenticated
