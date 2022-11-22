from rest_framework import serializers
from .models import register, User
from .utils import otp_generator


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
        user = User.objects.create_user(**validated_data)
        otp = otp_generator(user)
        user.otp = otp
        user.save()
        return user

    def validate(self, validated_data):
        if User.objects.filter(email=validated_data.get('email', '')).exists():
            raise Exception('Email Already exists')
        elif User.objects.filter(username=validated_data.get('username', '')).exists():
            raise Exception('Username Already exists')

        return validated_data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    class Meta:
        fields = ['email', 'password']

class EmailVerificationSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField(max_length=20,allow_blank=True)
    class Meta:
        fields=["email",'otp']

    def create(self, user):
        otp = otp_generator(user)
        user.otp = otp
        user.save()
        return user

    def validate(self, validated_data):
        if User.objects.filter(email=validated_data.get('email', '')).exists():
            return validated_data
        else:
            return Exception('Email does not Exists,PlZ Check Once')