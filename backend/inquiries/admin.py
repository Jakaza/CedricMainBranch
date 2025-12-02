from django.contrib import admin
from .models import ContactMessage, QuoteRequest

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'city', 'budget', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'city')
    list_filter = ('budget', 'created_at')
    readonly_fields = ('created_at',)
