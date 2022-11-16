from rest_framework import serializers
from .models import register

class registerserializers(serializers.Serializer):
    email=serializers.EmailField(max_length=100)
    user_name=serializers.CharField(max_length=50)
    phone_number=serializers.IntegerField()
    password=serializers.CharField(max_length=8,default=True)

    def create(self, validated_data):
         register.create(validated_data)