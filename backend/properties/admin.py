from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django_json_widget.widgets import JSONEditorWidget
from .models import Property, PropertyImage
from .widgets import DynamicTagWidget


class PropertyAdminForm(forms.ModelForm):
    """
    Custom form for Property admin with specialized widgets for JSON fields.
    """
    class Meta:
        model = Property
        fields = '__all__'
        widgets = {
            'styles': DynamicTagWidget(placeholder='Add a style (e.g., Modern)'),
            'features': DynamicTagWidget(placeholder='Add a feature (e.g., Open Plan)'),
            'amenities': DynamicTagWidget(placeholder='Add an amenity (e.g., Swimming Pool)'),
            'floors': DynamicTagWidget(placeholder='Add a floor (e.g., Ground Floor)'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make basic information fields required
        self.fields['title'].required = True
        self.fields['category'].required = True
        self.fields['price'].required = True
        
        # Make property specification fields required
        self.fields['bedrooms'].required = True
        self.fields['bathrooms'].required = True
        self.fields['garage'].required = True
        self.fields['floor_area'].required = True
        self.fields['levels'].required = True
        self.fields['width'].required = True
        self.fields['depth'].required = True
        
        # Styles is required
        self.fields['styles'].required = True
    
    def _clean_tag_field(self, field_name):
        """Helper method to clean comma-separated tag fields"""
        value = self.cleaned_data.get(field_name)
        
        if not value or value == '':
            return []
        
        # If it's already a list, return it
        if isinstance(value, list):
            return value
        
        # If it's a string, split by comma
        if isinstance(value, str):
            items = [item.strip() for item in value.split(',') if item.strip()]
            return items
        
        return []
    
    def clean_styles(self):
        """Convert comma-separated styles to list"""
        return self._clean_tag_field('styles')
    
    def clean_features(self):
        """Convert comma-separated features to list"""
        return self._clean_tag_field('features')
    
    def clean_amenities(self):
        """Convert comma-separated amenities to list"""
        return self._clean_tag_field('amenities')
    
    def clean_floors(self):
        """Convert comma-separated floors to list"""
        return self._clean_tag_field('floors')



class PropertyImageInline(admin.TabularInline):
    """
    Inline admin for property images with preview functionality.
    """
    model = PropertyImage
    extra = 1
    min_num = 1  # Require at least one image
    validate_min = True
    fields = ('image', 'image_preview', 'order')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        """
        Display a thumbnail preview of the uploaded image.
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "No image"
    
    image_preview.short_description = 'Preview'



@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Property model with organized fieldsets and custom widgets.
    """
    form = PropertyAdminForm
    list_display = (
        'title', 
        'category', 
        'price', 
        'bedrooms', 
        'bathrooms', 
        'garage',
        'floor_area',
        'is_new', 
        'is_popular',
        'created_at'
    )
    list_filter = (
        'category', 
        'is_new', 
        'is_popular', 
        'bedrooms', 
        'bathrooms',
        'garage',
        'pet_friendly',
        'created_at'
    )
    search_fields = ('title', 'description')
    list_editable = ('is_new', 'is_popular')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'price', 'description')
        }),
        ('Property Specifications', {
            'fields': (
                ('bedrooms', 'bathrooms', 'garage'),
                ('floor_area', 'levels'),
                ('width', 'depth'),
            )
        }),
        ('Additional Features', {
            'fields': (
                ('en_suite', 'lounges', 'dining_areas'),
                ('garage_parking', 'covered_parking'),
                'pet_friendly',
            ),
            'classes': ('collapse',)
        }),
        ('Design & Amenities', {
            'fields': ('styles', 'features', 'amenities', 'floors'),
            'description': 'Add tags one by one using the "+ Add" button. You can add as many or as few as you need.'
        }),
        ('Media', {
            'fields': ('video_url',)
        }),
        ('Display Options', {
            'fields': ('is_new', 'is_popular'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [PropertyImageInline]
    
    def get_queryset(self, request):
        """
        Optimize queryset with prefetch for better performance.
        """
        qs = super().get_queryset(request)
        return qs.prefetch_related('images')
