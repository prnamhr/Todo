from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        print(obj.created_by)
        return obj.created_by == request.user
class IsComment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True
