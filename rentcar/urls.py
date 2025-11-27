from django.urls import path
from .views import (
    CarModelAPIView,
    RegisterView,
    CategoryModelAPIView,
    CarDetailAPIView, CategoryDetailAPIView, CarListAPIView, CommentListCreateAPIView, PaymentAPIView, BookingAPIView,
    BookingDetailAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('comments/', CommentListCreateAPIView.as_view(), name='comments-list-create'),
    # CATEGORY LIST + CREATE
    path("categories/", CategoryModelAPIView.as_view()),
    path("categories/<int:pk>/", CategoryDetailAPIView.as_view()),

    # CAR LIST + CREATE
    path('cars/', CarModelAPIView.as_view(), name='car-models'),

    # CAR DETAIL (GET, PUT, DELETE)
    path('cars/<int:pk>/', CarDetailAPIView.as_view(), name='car-detail'),

    path('cars/filter/', CarListAPIView.as_view(), name='car-filter'),

    path("rent/<int:pk>/pay/", PaymentAPIView.as_view(), name="pay"),
    path("rent/", BookingAPIView.as_view(), name="booking-list-create"),
    path("rent/<int:pk>/", BookingDetailAPIView.as_view(), name="booking-detail"),

    # AUTH
    path('api/register/', RegisterView.as_view()),
    path('api/login/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
