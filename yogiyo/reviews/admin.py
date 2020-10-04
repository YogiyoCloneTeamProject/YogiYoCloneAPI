from django.contrib import admin
from django.utils.safestring import mark_safe

from reviews.models import *


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage


class OwnerCommentInline(admin.TabularInline):
    model = OwnerComment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'restaurant']
    inlines = [ReviewImageInline, OwnerCommentInline]


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']
    readonly_fields = ['preview_image']

    def preview_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.image.url,
            width=obj.image.width,
            height=obj.image.height)
        )


@admin.register(OwnerComment)
class OwnerCommentAdmin(admin.ModelAdmin):
    list_display = ['id']
