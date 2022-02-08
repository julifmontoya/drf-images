from rest_framework.permissions import AllowAny
from .serializers import TourImageSerializer, TourListSerializer, TourSerializer
from .models import Tour, TourImage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from decouple import config
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse


class TourListProv(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        tour = Tour.objects.all()
        serializer = TourListSerializer(tour, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TourSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class TourImageCreate(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, id):
        try:
            tour = Tour.objects.get(id=id)

            if(TourImage.objects.filter(tour=tour)):
                return Response({'error': 'you have already uploaded images'}, status=status.HTTP_400_BAD_REQUEST)

            # Create Gallery
            form_data = {}
            response = []

            for image in request.FILES.getlist('image'):
                form_data['image'] = image
                serializer = TourImageSerializer(data=form_data)

                if serializer.is_valid():
                    serializer.save(tour=tour)
                    response.append(serializer.data)
                else:
                    return Response(serializer.errors)

            return Response(response, status=status.HTTP_201_CREATED)

        except ValidationError:
            return Response({'error': 'Not Valid'}, status=status.HTTP_400_BAD_REQUEST)


class TourImageDetail(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, id):
        try:
            image_tour = TourImage.objects.filter(tour=id)
            serializer = TourImageSerializer(image_tour, many=True)
            return JsonResponse(serializer.data, safe=False)

        except ValidationError:
            return Response({'error': 'Not Valid'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            tour = Tour.objects.get(id=id)

            # Delete Image from database
            for tour_image in TourImage.objects.filter(tour=tour):
                tour_image.image.delete()
                tour_image.delete()

            # Create Gallery
            form_data = {}
            response = []

            for image in request.FILES.getlist('image'):
                form_data['image'] = image
                serializer = TourImageSerializer(data=form_data)

                if serializer.is_valid():
                    serializer.save(tour=tour)
                    response.append(serializer.data)
                else:
                    return Response(serializer.errors)

            return Response(response, status=status.HTTP_201_CREATED)

        except ValidationError:
            return Response({'error': 'Not Valid'}, status=status.HTTP_400_BAD_REQUEST)


class TourDetailProv(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, id):
        try:
            tour = Tour.objects.get(id=id)

        except Tour.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = TourSerializer(tour)
        return Response(serializer.data)

    def put(self, request, id):
        try:
            tour = Tour.objects.get(id=id)
            serializer = TourSerializer(tour, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Tour.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
