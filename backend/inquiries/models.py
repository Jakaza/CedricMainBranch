from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.name}"

class QuoteRequest(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    
    preferred_style = models.CharField(max_length=100)
    custom_style = models.CharField(max_length=255, blank=True)
    
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    other_rooms = models.TextField(blank=True)
    
    yard_length = models.DecimalField(max_digits=8, decimal_places=2)
    yard_breadth = models.DecimalField(max_digits=8, decimal_places=2)
    
    budget = models.CharField(max_length=100)
    description = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quote for {self.full_name}"
