from rest_framework import permissions

class IsAdminBojnourd(permissions.BasePermission):
    def has_permission(self, request, view):
        # return request.user.is_authenticated and request.user.is_superuser and request.phone.startwith('0935')
        return (
            request.user.is_authenticated
            and request.user.is_superuser
            and request.user.phone.startswith('0935')
        )
    

class IsBuyer(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.buyer == request.user
