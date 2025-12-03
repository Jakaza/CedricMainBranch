from rest_framework import serializers
from .models import SiteSettings, ContactInformation, TeamMember, Testimonial

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'

class ContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = '__all__'

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'
