from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Product

# Register Products
admin.site.register(Product)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    list_display = (
        "email",
        "first_name",
        "last_name",
        "start_date",
        "is_active",
        "is_staff",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "start_date",
        "is_active",
        "is_staff",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("start_date",)

    filter_horizontal = ("products",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "about")}),
        ("Products", {"fields": ("products",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "about",
                    "is_staff",
                ),
            },
        ),
    )
