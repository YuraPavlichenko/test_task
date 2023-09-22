from rest_framework import serializers
from .models import Restaurant, Menu, Employee
from datetime import date


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name']


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['dish_name', 'restaurant', 'price', 'day_of_week', 'date']

    def validate(self, data):
        chosen_date = data['date']

        today = date.today()
        if chosen_date < today:
            raise serializers.ValidationError("It is not possible to add menus for past days")

        chosen_day = data['day_of_week']

        if chosen_date.strftime('%A') != chosen_day:
            raise serializers.ValidationError("The selected day does not match the selected date")

        return data


class RestaurantMenuListSerializer(serializers.ModelSerializer):
    day_of_week = serializers.CharField(source='get_day_of_week_display')

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'dish_name', 'price', 'votes', 'day_of_week', 'date']


class MenuByDaySerializer(serializers.Serializer):
    dish_name = serializers.CharField()
    restaurant_name = serializers.CharField(source='restaurant.name')
    date = serializers.DateField()
    dish_id = serializers.IntegerField(source='id')


class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('username', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = Employee(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user


class VoteSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField()
    restaurant_id = serializers.IntegerField()


class WinningMenuSerializer(serializers.Serializer):
    dish_name = serializers.CharField()
    restaurant_name = serializers.CharField(source='restaurant.name')
    votes = serializers.IntegerField()