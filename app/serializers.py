from rest_framework import serializers
from .models import MyUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'password']

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['weather data']