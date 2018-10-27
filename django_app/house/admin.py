from django.contrib import admin

from .models import House, Images


class PropertyImageInline(admin.TabularInline):
    model = Images
    extra = 5


class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline, ]


admin.site.register(House, PropertyAdmin)
