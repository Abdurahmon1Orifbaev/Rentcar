from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView

from rentcar.models.booking import Booking
from rentcar.models.car_model import Car
from rentcar.models.category import Category
from rentcar.models.comments import Comment
from rentcar.serializer import RegisterSerializer, CategorySerializer, CarSerializer, CommentSerializer, \
    BookingSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class CategoryModelAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer




class CarModelAPIView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer



class CarListAPIView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        category_ids = params.getlist("category")
        if len(category_ids) == 1 and "," in category_ids[0]:
            category_ids = category_ids[0].split(",")

        if category_ids:
            queryset = queryset.filter(category_id__in=category_ids)

        seats = params.getlist("seats")

        seats_filter = []
        seats_more_than_8 = False

        for s in seats:
            if s == "8+":
                seats_more_than_8 = True
            else:
                seats_filter.append(int(s))

        if seats_filter:
            queryset = queryset.filter(seats__in=seats_filter)

        if seats_more_than_8:
            queryset = queryset.filter(seats__gte=8)

        max_price = params.get("max_price")
        if max_price:
            queryset = queryset.filter(price_per_day__lte=max_price)

        return queryset



class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class PaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        # Simulate payment success
        booking.payment_status = "paid"
        booking.save()

        return Response({
            "message": "Payment successful",
            "booking_id": booking.id,
            "status": booking.payment_status
        })



class BookingAPIView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        car = serializer.validated_data["car"]
        start = serializer.validated_data["start_date"]
        end = serializer.validated_data["end_date"]

        days = (end - start).days
        if days <= 0:
            raise ValidationError("End date must be after start date.")

        total = car.final_price * days

        serializer.save(
            user=self.request.user,
            total_price=total
        )


class BookingDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

