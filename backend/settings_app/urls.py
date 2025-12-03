from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SiteSettingsView, 
    ContactInformationView, 
    TeamMemberViewSet, 
    TestimonialViewSet,
    ServiceViewSet,
    PlanModificationViewSet,
    WhyTrustUsViewSet,
    CertificationViewSet
)

router = DefaultRouter()
router.register(r'team', TeamMemberViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'plan-modifications', PlanModificationViewSet)
router.register(r'why-trust-us', WhyTrustUsViewSet)
router.register(r'certifications', CertificationViewSet)

urlpatterns = [
    path('settings/', SiteSettingsView.as_view(), name='site-settings'),
    path('contact-info/', ContactInformationView.as_view(), name='contact-info'),
    path('', include(router.urls)),
]

