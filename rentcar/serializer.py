from rest_framework import serializers
from django.contrib.auth.models import User

from rentcar.models.booking import Booking
from rentcar.models.car_model import Car
from rentcar.models.category import Category
from rentcar.models.comments import Comment


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        return user



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"




class CarSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = '__all__'


    def get_final_price(self, obj):
        return obj.price_per_day




class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Shows username instead of id

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'rating', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ("user", "total_price", "payment_status")

    def create(self, validated_data):
        # Calculate total_price
        car = validated_data["car"]
        start_date = validated_data["start_date"]
        end_date = validated_data["end_date"]
        days = (end_date - start_date).days + 1
        total_price = car.price_per_day * days

        # Remove fields that are manually set
        validated_data.pop("user", None)
        validated_data.pop("total_price", None)
        validated_data.pop("payment_status", None)

        booking = Booking.objects.create(
            user=self.context["request"].user,
            total_price=total_price,
            payment_status="pending",
            **validated_data
        )
        return booking
