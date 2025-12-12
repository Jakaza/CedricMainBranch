from django.db import models
from django.core.exceptions import ValidationError

class SingletonModel(models.Model):
    """Abstract model that ensures only one instance exists."""
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError(f"There can be only one {self._meta.verbose_name} instance")
        return super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        if cls.objects.exists():
            return cls.objects.first()
        return cls()

class SiteSettings(SingletonModel):
    company_name = models.CharField(max_length=100, default="Cedric House Designs")
    tagline = models.CharField(max_length=255, default="Crafting exceptional homes and dreams")
    hero_title = models.CharField(max_length=255, default="Find Your Perfect House Plan")
    hero_description = models.TextField(default="Discover thousands of professionally designed house plans. From modern minimalist to classic traditional styles.")
    
    # About Page Content
    about_title = models.CharField(max_length=255, default="About Cedric House Designs")
    about_description = models.TextField(default="Crafting exceptional homes and dreams for over two decades.")
    who_we_are_content = models.TextField(default="Cedric House Designs is a leading architectural firm...")
    mission_statement = models.TextField(default="To design and deliver exceptional residential homes...")
    
    # Stats
    years_experience = models.CharField(max_length=50, default="25+")
    projects_completed = models.CharField(max_length=50, default="500+")
    client_satisfaction = models.CharField(max_length=50, default="98%")
    
    class Meta:
        verbose_name = "Site Settings (Homepage)"
        verbose_name_plural = "Site Settings (Homepage)"

    def __str__(self):
        return "Site Settings"

class ContactInformation(SingletonModel):
    phone_number = models.CharField(max_length=50, default="+27 (0) 72 665 9790")
    email = models.EmailField(default="info@cedrichouseplans.co.za")
    support_email = models.EmailField(default="support@cedrichouseplans.co.za")
    address = models.TextField(default="South Africa")
    
    # Operating Hours
    monday_friday = models.CharField(max_length=100, default="9:00 AM - 6:00 PM")
    saturday = models.CharField(max_length=100, default="10:00 AM - 4:00 PM")
    sunday = models.CharField(max_length=100, default="Closed")
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Contact Information"
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return "Contact Information"

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    experience = models.CharField(max_length=50)
    specialty = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Team Member (About Page)"
        verbose_name_plural = "Team Members (About Page)"

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default="Verified Customer")
    content = models.TextField()
    rating = models.IntegerField(default=5)
    initials = models.CharField(max_length=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Testimonial (Homepage)"
        verbose_name_plural = "Testimonials (Homepage)"
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"

class Service(models.Model):
    """Service offerings displayed on the Services page."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    badge = models.CharField(max_length=50, blank=True, help_text="Optional badge text (e.g., 'Popular', 'Premium', 'Technical')")
    icon_name = models.CharField(max_length=50, help_text="Lucide icon name (e.g., 'Home', 'Pencil', 'Eye')")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Service (Services Page)"
        verbose_name_plural = "Services (Services Page)"
    
    def __str__(self):
        return self.title

class PlanModification(models.Model):
    """Plan modification features displayed on the Services page."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Plan Modification (Services Page)"
        verbose_name_plural = "Plan Modifications (Services Page)"
    
    def __str__(self):
        return self.title

class WhyTrustUs(models.Model):
    """Trust indicators displayed on the About page."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Why Trust Us Item (About Page)"
        verbose_name_plural = "Why Trust Us (About Page)"
    
    def __str__(self):
        return self.title

class Certification(models.Model):
    """Certifications and credentials displayed on the About page."""
    name = models.CharField(max_length=200)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Certification (About Page)"
        verbose_name_plural = "Certifications (About Page)"
    
    def __str__(self):
        return self.name
