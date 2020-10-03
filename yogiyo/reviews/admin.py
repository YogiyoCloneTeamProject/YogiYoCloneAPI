from django.contrib import admin
from reviews.models import *


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage


class OwnerCommentInline(admin.TabularInline):
    model = OwnerComment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'restaurant']
    inlines = [ReviewImageInline, OwnerCommentInline]
