from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    list_display = ['username', 'email', 'display_name', 'role', 'is_staff']
    list_filter = UserAdmin.list_filter + ('role',)

    fieldsets = UserAdmin.fieldsets + (
        ('Role & Preferences', {
            'fields': ('role', 'display_name'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role & Preferences', {
            'fields': ('role', 'display_name'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.role == CustomUser.Roles.ADMIN:
            obj.is_staff = True
        super().save_model(request, obj, form, change)