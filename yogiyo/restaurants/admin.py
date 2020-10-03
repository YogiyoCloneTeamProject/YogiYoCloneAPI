from django.contrib import admin

from core.admin import CustomModelAdmin
from restaurants.models import *


class MenuGroupInline(admin.TabularInline):
    model = MenuGroup


class MenuInline(admin.TabularInline):
    model = Menu


class OptionGroupInline(admin.TabularInline):
    model = OptionGroup


class OptionInline(admin.TabularInline):
    model = Option


@admin.register(Restaurant)
class RestaurantAdmin(CustomModelAdmin):
    list_display = ['id', 'name']
    inlines = [MenuGroupInline]


@admin.register(MenuGroup)
class MenuGroupAdmin(CustomModelAdmin):
    list_display = ['id', 'name']
    inlines = [MenuInline]


@admin.register(Menu)
class MenuAdmin(CustomModelAdmin):
    list_display = ['id', 'name', 'price']
    inlines = [OptionGroupInline]


@admin.register(OptionGroup)
class OptionGroupAdmin(CustomModelAdmin):
    list_display = ['id', 'name', 'mandatory']
    inlines = [OptionInline]


@admin.register(Option)
class OptionAdmin(CustomModelAdmin):
    list_display = ['id', 'name', 'price']
