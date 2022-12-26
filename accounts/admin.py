from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import UserAdminChangeForm,UserAdminCreationForm
User=get_user_model()

class UserAdmin(UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    readonly_fields=("password",)
    fieldsets = (
        (None, {"fields": ("username","email", "password","password_reset_token","password_reset_token_expire")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username","email", "password1", "password2"),
            },
        ),
    )
    
    # change_password_form = AdminPasswordChangeForm
    list_display = ("id","username", "email",  "is_staff","is_superuser")
    list_filter = ("is_active",)
    search_fields = ("username", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
admin.site.register(User, UserAdmin)