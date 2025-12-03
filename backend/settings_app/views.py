from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SiteSettings, ContactInformation, TeamMember, Testimonial
from .serializers import (
    SiteSettingsSerializer, 
    ContactInformationSerializer, 
    TeamMemberSerializer, 
    TestimonialSerializer
)

class SiteSettingsView(APIView):
    """
    Retrieve the site settings.
    """
    def get(self, request):
        settings = SiteSettings.load()
        serializer = SiteSettingsSerializer(settings)
        return Response(serializer.data)

class ContactInformationView(APIView):
    """
    Retrieve the contact information.
    """
    def get(self, request):
        contact_info = ContactInformation.load()
        serializer = ContactInformationSerializer(contact_info)
        return Response(serializer.data)

class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List team members.
    """
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer

class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List active testimonials.
    """
    queryset = Testimonial.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = TestimonialSerializer
