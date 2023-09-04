from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        print(request.user.is_staff,request.user)
        return request.user and request.user.is_staff

class IsStaffUserOrCreate(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_staff

class ProfilePermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff