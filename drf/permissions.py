from rest_framework.permissions import BasePermission


class OwnerPerms(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.pk == obj.owner:
            return True
        return False


class ModerPerms(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE']:
            return False
        return request.user.is_staff


class SuperPerms(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser
