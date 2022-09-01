from rest_framework import permissions


class AccessProductOne(permissions.BasePermission):
    message = "Not allowed to access this product"

    def has_permission(self, request, view):
        # Check if staff
        if request.user.is_staff:
            return True
        # Check if has Product with the correct slug
        if request.user.products.filter(slug="product_one").exists():
            return True
        return False


class AccessProductTwo(permissions.BasePermission):
    message = "Not allowed to access this product"

    def has_permission(self, request, view):
        # Check if staff
        if request.user.is_staff:
            return True
        # Check if has Product with the correct slug
        if request.user.products.filter(slug="product_two").exists():
            return True
        return False
