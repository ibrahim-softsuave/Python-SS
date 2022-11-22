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
from .tasks import send_email_for_otp_verification
from Learning.constant import RESPONSE_DATA
from Test.utils import upload_file
from copy import deepcopy


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
        response_data = deepcopy(RESPONSE_DATA)
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if user_data.get('password') != user_data.get('confirm_password'):
            response_data['message'] = "Password and Confirm password doesn't match"
            return Response(response_data, status=status.BAD_REQUEST)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            response_data['message'] = str(e)
            return Response(response_data, status=status.BAD_REQUEST)

        serializer.save()
        send_email_for_otp_verification.delay(user_data)
        response_data = dict(
            message='User Created Successfully',
            status='Success',
            statusCode=201
        )
        return Response(response_data, status=status.CREATED)


class LoginAPI(generics.ListCreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        response_data = deepcopy(RESPONSE_DATA)
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            response_data['message'] = str(e)
            return Response(response_data, status=status.BAD_REQUEST)
        user = auth.authenticate(
            email=user_data.get('email'),
            password=user_data.get('password')
        )
        if not user:
            response_data['message'] = "User doesn't exist"
            return Response(response_data, status=status.BAD_REQUEST)
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


class FileUploadAPI(generics.ListCreateAPIView):
    def post(self, request):
        response_data = deepcopy(RESPONSE_DATA)
        file = request.data.get('file')
        if not file:
            response_data['message'] = "File not found"
            return Response(response_data, status=status.BAD_REQUEST)
        file_path = upload_file(file)
        response_data['message'] = "File uploaded successfully"
        response_data['filePath'] = file_path
        
        return Response(RESPONSE_DATA, status=status.OK)
