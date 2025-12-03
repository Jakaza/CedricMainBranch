from django.contrib import admin
from .models import SiteSettings, ContactInformation, TeamMember, Testimonial

class SingletonAdmin(admin.ModelAdmin):
    """Admin class for Singleton models."""
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ('General', {
            'fields': ('company_name', 'tagline')
        }),
        ('Hero Section', {
            'fields': ('hero_title', 'hero_description')
        }),
        ('About Page', {
            'fields': ('about_title', 'about_description', 'who_we_are_content', 'mission_statement')
        }),
        ('Statistics', {
            'fields': ('years_experience', 'projects_completed', 'client_satisfaction')
        })
    )

@admin.register(ContactInformation)
class ContactInformationAdmin(SingletonAdmin):
    fieldsets = (
        ('Contact Details', {
            'fields': ('phone_number', 'email', 'support_email', 'address')
        }),
        ('Operating Hours', {
            'fields': ('monday_friday', 'saturday', 'sunday')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url')
        })
    )

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'role')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'is_active')
    list_filter = ('rating', 'is_active')
    search_fields = ('name', 'content')
