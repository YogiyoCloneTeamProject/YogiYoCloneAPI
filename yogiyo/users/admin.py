"""Integrate with admin module."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, Profile


class ProfileInline(admin.TabularInline):
    model = Profile


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    # fieldsets = (
    #     (None, {'fields': ('email', 'password')}),
    #     (_('Personal info'), {'fields': ('first_name', 'last_name')}),
    #     (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
    #                                    'groups', 'user_permissions')}),
    #     (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password1', 'password2'),
    #     }),
    # )
    list_display = ('email', 'nickname', 'phone_nun', 'is_active')
    search_fields = ('email', 'profile__nickname')
    ordering = ('email',)
    inlines = [ProfileInline]

    def nickname(self, user):
        return user.profile.nickname

    def phone_nun(self, user):
        return user.profile.phone_nun
