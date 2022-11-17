from rest_framework import serializers
from .models import register, User

class registerserializers(serializers.Serializer):
    email=serializers.EmailField(max_length=100)
    user_name=serializers.CharField(max_length=50)
    phone_number=serializers.IntegerField()
    password=serializers.CharField(max_length=8,default=True)

    def create(self, validated_data):
         register.create(validated_data)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=30, min_length=8)
    password = serializers.CharField(max_length=30, min_length=8)
    confirm_password = serializers.CharField(max_length=30, min_length=8)
    
    class Meta:
        fields = ['email', 'password', 'confirm_password']

    def create(self, validated_data):
        del validated_data['confirm_password']
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    class Meta:
        fields = ['email', 'password']