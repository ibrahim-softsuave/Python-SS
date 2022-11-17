from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from .models import register
from .serializers import registerserializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from django.contrib import auth
from rest_framework.response import Response 
from Test.serializers import RegisterSerializer, LoginSerializer
from http import HTTPStatus as status
from rest_framework_simplejwt.tokens import RefreshToken
from Test.models import User
from fernet import Fernet


# Create your views here.
@csrf_exempt
def Home(request):
    if request.method=="GET":
        registers=register.objects.all()
        serializer=registerserializers(registers,many=True)
        return JsonResponse(serializer.data,safe=False)
    elif request.method=="POST":
        data=JSONParser().parse(request)
        serializer=registerserializers(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
            
        return JsonResponse(serializer.errors,status=400)


class RegisterAPI(generics.ListCreateAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        try:
            user_data = request.data
            serializer = self.serializer_class(data=user_data)
            if user_data.get('password') != user_data.get('confirm_password'):
                return Response("Password and Confirm password doesn't match", status=status.BAD_REQUEST)
            try:
                serializer.is_valid(raise_exception=True)
            except Exception as e:
                return Response(str(e), status=status.BAD_REQUEST)

            serializer.save()
            response_data = dict(
                message='User Created Successfully',
                status='Success',
                statusCode=201
            )
            return Response(response_data, status=status.CREATED)
        except Exception as e:
            return Response(str(e), status=status.BAD_REQUEST)


class LoginAPI(generics.ListCreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            user_data = request.data
            serializer = self.serializer_class(data=user_data)
            try:
                serializer.is_valid(raise_exception=True)
            except Exception as e:
                return Response(str(e), status=status.BAD_REQUEST)
            user = auth.authenticate(
                email=user_data.get('email'),
                password=user_data.get('password')
            )
            if not user:
                return Response("User doesn't exist", status=status.BAD_REQUEST)
            refresh_token = RefreshToken.for_user(user)
            response_data = dict(
                message='Logged In Successfully',
                status='Success',
                statusCode=200,
                email=user.email,
                username=user.username,
                token={
                    'refresh_token': str(refresh_token),
                    'access_token': str(refresh_token.access_token)
                }
            )
            return Response(response_data, status=status.OK)
        except Exception as e:
            return Response(str(e), status=status.BAD_REQUEST)
