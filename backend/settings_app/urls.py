from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SiteSettingsView, 
    ContactInformationView, 
    TeamMemberViewSet, 
    TestimonialViewSet
)

router = DefaultRouter()
router.register(r'team', TeamMemberViewSet)
router.register(r'testimonials', TestimonialViewSet)

urlpatterns = [
    path('settings/', SiteSettingsView.as_view(), name='site-settings'),
    path('contact-info/', ContactInformationView.as_view(), name='contact-info'),
    path('', include(router.urls)),
]
