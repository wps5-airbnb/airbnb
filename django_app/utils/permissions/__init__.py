from rest_framework import permissions


class IsHouseOwner(permissions.BasePermission):
    """
    유저가 변경하려는 House가 자기 자신의 House인지 검사
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.host == request.user