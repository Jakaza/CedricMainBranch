from django.contrib import admin
from .models import SiteSettings, ContactInformation, TeamMember, Testimonial, Service, PlanModification, WhyTrustUs, Certification

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
        ('General Settings (Site-wide)', {
            'fields': ('company_name', 'tagline'),
            'description': 'These settings appear across the entire website'
        }),
        ('Hero Section (Homepage)', {
            'fields': ('hero_title', 'hero_description'),
            'description': 'Main banner section on the homepage'
        }),
        ('About Page Content', {
            'fields': ('about_title', 'about_description', 'who_we_are_content', 'mission_statement'),
            'description': 'Content displayed on the About page'
        }),
        ('Statistics (About Page)', {
            'fields': ('years_experience', 'projects_completed', 'client_satisfaction'),
            'description': 'Statistics displayed on the About page'
        })
    )

@admin.register(ContactInformation)
class ContactInformationAdmin(SingletonAdmin):
    fieldsets = (
        ('Contact Details (Contact Page & Footer)', {
            'fields': ('phone_number', 'email', 'support_email', 'address'),
            'description': 'Contact information displayed on Contact page and site footer'
        }),
        ('Operating Hours (Contact Page)', {
            'fields': ('monday_friday', 'saturday', 'sunday'),
            'description': 'Business hours displayed on the Contact page'
        }),
        ('Social Media Links (Footer)', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url'),
            'description': 'Social media links displayed in the site footer'
        })
    )

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'role')
    
    class Meta:
        help_text = "Team members displayed on the About page"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'is_active')
    list_filter = ('rating', 'is_active')
    search_fields = ('name', 'content')
    
    class Meta:
        help_text = "Customer testimonials displayed on the Homepage"

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'badge')
    search_fields = ('title', 'description')
    ordering = ('order',)
    
    class Meta:
        help_text = "Service offerings displayed on the Services page"

@admin.register(PlanModification)
class PlanModificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')
    ordering = ('order',)
    
    class Meta:
        help_text = "Plan modification features displayed on the Services page"

@admin.register(WhyTrustUs)
class WhyTrustUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')
    ordering = ('order',)
    
    class Meta:
        help_text = "Trust indicators displayed on the About page"

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    ordering = ('order',)
    
    class Meta:
        help_text = "Certifications and credentials displayed on the About page"
