from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User, Profile


class ProfileInline(admin.TabularInline):
    model = Profile


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'email', 'nickname', 'phone_num', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email', 'profile__nickname')
    ordering = ('id',)
    inlines = [ProfileInline]

    def nickname(self, user):
        return user.profile.nickname

    def phone_num(self, user):
        return user.profile.phone_num
