from rest_framework import permissions

from apps.users.models import UserRole


class CanManagePurchaseOrders(permissions.BasePermission):
    """
    Admin and Procurement Officer can create/update purchase orders.
    Others can only read.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.role in {
            UserRole.ADMIN,
            UserRole.PROCUREMENT_OFFICER,
        }


class CanApprovePurchaseOrders(permissions.BasePermission):
    """
    Only Admin can approve or reject purchase orders.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )


class CanCompletePurchaseOrders(permissions.BasePermission):
    """
    Admin and Procurement Officer can mark approved purchase orders as completed.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role
            in {
                UserRole.ADMIN,
                UserRole.PROCUREMENT_OFFICER,
            }
        )