from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet, QuoteRequestViewSet

router = DefaultRouter()
router.register(r'contact', ContactMessageViewSet)
router.register(r'quotes', QuoteRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
