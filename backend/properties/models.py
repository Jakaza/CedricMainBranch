from django.db import models

class Property(models.Model):
    CATEGORY_CHOICES = [
        ('PLAN', 'House Plan'),
        ('BUILT', 'Built Home'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='PLAN')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    garage = models.IntegerField(default=0)
    floor_area = models.IntegerField(default=0)
    levels = models.IntegerField(default=0)
    width = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    depth = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    # JSON fields for lists
    styles = models.JSONField(default=list, blank=True)
    features = models.JSONField(default=list, blank=True)
    amenities = models.JSONField(default=list, blank=True)
    floors = models.JSONField(default=list, blank=True)
    room_specifications = models.JSONField(default=list, blank=True)  # Custom room types with quantities
    
    is_new = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    
    # Optional fields
    en_suite = models.IntegerField(default=0)
    lounges = models.IntegerField(default=0)
    dining_areas = models.IntegerField(default=0)
    garage_parking = models.IntegerField(default=0)
    covered_parking = models.IntegerField(default=0)
    pet_friendly = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Property (Built Homes / House Plans Page)"
        verbose_name_plural = "Properties (Built Homes / House Plans Page)"

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.property.title}"
