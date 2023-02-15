from .models import *
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password"
        ]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = "__all__"


class GroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ground
        fields = "__all__"

class PitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitch
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Booking
        fields = "__all__"

class LeagueSerializer(serializers.ModelSerializer):

    class Meta:
        model = League
        fields = "__all__"

class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teams
        fields = "__all__"

class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = "__all__"






        # depth = 1

    # instance = Booking.objects.all()
    # for i in instance:
    #     print(i)
    # # print(instance.values())
    # def find_total(self, Booking):
    #     return Booking.bookingdate_id.timeslot.price

class BookingDateSerializer(serializers.ModelSerializer):
    # price = serializers.SerializerMethodField(method_name = "total_price")
    class Meta:
        model = BookingDates
        fields = "__all__"
        


    # def total_price():
    #     instance = BookingDates.objects.all()
    #     sum = 0
    #     for i in instance:
    #         value = i.timeslot.price
    #         sum = sum + value
           
    #     return sum