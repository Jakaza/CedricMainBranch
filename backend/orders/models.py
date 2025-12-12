from django.db import models
from properties.models import Property

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    )

    plan = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='orders')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    yoco_checkout_id = models.CharField(max_length=100, blank=True, null=True)
    yoco_payment_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Customer Details (optional, can be expanded)
    customer_email = models.EmailField(blank=True, null=True)
    
    # Receipt tracking
    receipt_generated = models.BooleanField(default=False)
    receipt_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    
    class Meta:
        verbose_name = "Order ( List of all orders )"
        verbose_name_plural = "Orders ( List of all orders )"
    
    def __str__(self):
        return f"Order #{self.id} - {self.plan.title} - {self.status}"
    
    def generate_receipt_number(self):
        """Generate a unique receipt number"""
        if not self.receipt_number:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d')
            self.receipt_number = f"RCP-{timestamp}-{self.id:05d}"
            self.save()
        return self.receipt_number
