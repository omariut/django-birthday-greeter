from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.user_type == 'admin'

class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.user_type == 'customer'

class IsObjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user
