from rest_framework import permissions

from .models import UserRole 

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRole.ADMIN)

class IsInventoryManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in {UserRole.ADMIN, UserRole.INVENTORY_MANAGER})

class IsProcurementOfficerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in {UserRole.ADMIN, UserRole.PROCUREMENT_OFFICER})

class IsAuditorReadOnly(permissions.BasePermission):
    """
    Auditors can only read; admins can do anything.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.role == UserRole.ADMIN:
            return True

        if request.user.role == UserRole.AUDITOR:
            return request.method in permissions.SAFE_METHODS

        return False