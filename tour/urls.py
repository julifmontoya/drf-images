from django.urls import path
from .views import TourImageCreate, TourImageDetail, TourListProv, TourDetailProv

urlpatterns = [
    path('tours/', TourListProv.as_view()),
    path('tours/<id>/', TourDetailProv.as_view()),
    path('tours-image-create/<id>/', TourImageCreate.as_view()),
    path('tours-image/<id>/', TourImageDetail.as_view()),
]
