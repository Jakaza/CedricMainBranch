from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Property
from .serializers import PropertySerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def get_queryset(self):
        queryset = Property.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    @action(detail=False, methods=['get'])
    def plans(self, request):
        queryset = self.get_queryset().filter(category='PLAN')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def built(self, request):
        queryset = self.get_queryset().filter(category='BUILT')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
