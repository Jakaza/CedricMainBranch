from rest_framework import viewsets
from .models import ContactMessage, QuoteRequest
from .serializers import ContactMessageSerializer, QuoteRequestSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

class QuoteRequestViewSet(viewsets.ModelViewSet):
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
