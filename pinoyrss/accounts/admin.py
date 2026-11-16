from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'preferred_regions', 'preferred_languages']
    fieldsets = UserAdmin.fieldsets + (
        ('Roles and Preferences', {'fields': ('role', 'preferred_regions', 'preferred_languages')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role & Preferences', {
            'fields': ('role', 'preferred_regions', 'preferred_languages'),
        }),
    )
    def save_model(self, request, obj, form, change):
        if obj.role == CustomUser.Roles.ADMIN:
            obj.is_staff = True
        super().save_model(request, obj, form, change)