from rest_framework.permissions import BasePermission



class IsSuperuser(BasePermission):
    """
    Allows access only to superusers
    """
    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_superuser
                    and request.user.is_staff)


class IsAdministrator(BasePermission):
    """
    Allows access only to administrators
    """
    def has_permission(self, request, view):

        return bool(request.user
                    and not request.user.is_superuser
                    and not request.user.is_trainer
                    and request.user.is_staff)


class IsCoach(BasePermission):
    """
    Allows access only to trainers(coaches)
    """
    def has_permission(self, request, view):
        return bool(request.user
                    and not request.user.is_superuser
                    and not request.user.is_staff
                    and request.user.is_trainer)


class IsClient(BasePermission):
    """
    Allows access only to trainers(coaches)
    """
    def has_permission(self, request, view):
        return bool(request.user
                    and not request.user.is_superuser
                    and not request.user.is_staff
                    and not request.user.is_trainer)


class IsVerified(BasePermission):
    """
    Allows access only to verified users (all types)
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_verified)


class IsActive(BasePermission):
    """
    Allows access only to active users (all types)
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)
