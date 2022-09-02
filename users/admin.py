from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Product, Subscription

# Register Product and Subscription models
admin.site.register(Product)
admin.site.register(Subscription)


# Create Inline
class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 1


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    list_display = (
        "email",
        "first_name",
        "last_name",
        "date_joined",
        "is_active",
        "is_staff",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "date_joined",
        "is_active",
        "is_staff",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "cellphone", "input_company_name", "about")}),
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

    inlines = [SubscriptionInline]

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
