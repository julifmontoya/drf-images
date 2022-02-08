
from rest_framework import serializers
from .models import Tour, TourImage
from decouple import config


class TourListSerializer(serializers.ModelSerializer):
    class Meta():
        model = Tour
        fields = '__all__'


class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        fields = ['image']


class TourSerializer(serializers.ModelSerializer):
    images = TourImageSerializer(many=True, read_only=True)
    class Meta():
        model = Tour
        fields = ['id', 'title', 'description', 'images']

        extra_kwargs = {
            "file_content": {
                "required": False,
            }
        }

    def to_representation(self, instance):
        link = config('HOST')
        images = []
        for image in instance.images.all():
            images.append({"image": f'{link}media/{image.image}'})


        return {
            'id': instance.id,
            'title': instance.title,
            'description': instance.description,
            'images': images
        }

