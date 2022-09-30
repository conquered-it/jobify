from rest_framework import permissions


class IsAdminUserOrApplicant(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        admin_permission = bool(request.user and request.user.is_staff)
        applicant_permission = bool(request.user and obj.id == request.user.id)
        return applicant_permission or admin_permission


class IsApplicant(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        applicant_permission = bool(request.user and obj.id == request.user.id)
        return applicant_permission


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.is_staff)

        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return admin_permission


class IsAdminUserOrApplicantReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        admin_permission = bool(request.user and request.user.is_staff)
        applicant_permission = bool(
            request.user and obj.applicant_id == request.user.id)
        if request.method in permissions.SAFE_METHODS:
            return admin_permission or applicant_permission
        else:
            return admin_permission
