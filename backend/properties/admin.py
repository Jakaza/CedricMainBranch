from django.contrib import admin
from .models import Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'bedrooms', 'bathrooms', 'is_new', 'is_popular')
    list_filter = ('category', 'is_new', 'is_popular', 'bedrooms', 'bathrooms')
    search_fields = ('title', 'description')
    inlines = [PropertyImageInline]
