from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a review to edit it.
    Anyone can read the reviews.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to create, edit, or delete reviews.
    Users can read reviews without restriction.
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser
