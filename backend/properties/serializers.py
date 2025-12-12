from rest_framework import serializers
from .models import Property, PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'order']

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    image_urls = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'category', 'price', 'bedrooms', 'bathrooms', 'garage',
            'floor_area', 'levels', 'width', 'depth', 'styles', 'features',
            'amenities', 'floors', 'room_specifications', 'is_new', 'is_popular', 
            'description', 'video_url', 'en_suite', 'lounges', 'dining_areas', 
            'garage_parking', 'covered_parking', 'pet_friendly', 'created_at', 
            'updated_at', 'images', 'uploaded_images', 'image_urls'
        ]

    def get_image_urls(self, obj):
        request = self.context.get('request')
        urls = []
        for img in obj.images.all():
            if img.image:
                if request:
                    urls.append(request.build_absolute_uri(img.image.url))
                else:
                    urls.append(img.image.url)
        return urls

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        property_obj = Property.objects.create(**validated_data)
        
        for i, image in enumerate(uploaded_images):
            PropertyImage.objects.create(property=property_obj, image=image, order=i)
            
        return property_obj
