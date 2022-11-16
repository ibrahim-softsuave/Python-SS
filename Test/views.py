from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from .models import register
from.serializers import registerserializers
from django.views.decorators.csrf import csrf_exempt

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