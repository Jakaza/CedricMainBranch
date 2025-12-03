from rest_framework import serializers
from .models import SiteSettings, ContactInformation, TeamMember, Testimonial, Service, PlanModification, WhyTrustUs, Certification

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'

class ContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = '__all__'

class TeamMemberSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = TeamMember
        fields = '__all__'
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class PlanModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanModification
        fields = '__all__'

class WhyTrustUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyTrustUs
        fields = '__all__'

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

