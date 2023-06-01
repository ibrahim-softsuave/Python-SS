from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse
from Learning import excluded_endpoints
from http import HTTPStatus as status
from rest_framework_simplejwt import exceptions
from Learning.constant import RESPONSE_DATA
from copy import deepcopy


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.response_data = deepcopy(RESPONSE_DATA)

    def __call__(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION')
        try:
            if request.path not in excluded_endpoints:
                if not access_token:
                    self.response_data['message'] = 'Unauthorized'
                    return HttpResponse(self.response_data, status=status.BAD_REQUEST)
                jwt_auth = JWTAuthentication()
                user, payload = jwt_auth.authenticate(request)
                request.payload = payload.payload
        
        except exceptions.InvalidToken as e:
            self.response_data['message'] = "Invalid Token or Token got expired"
            return HttpResponse(self.response_data, status=status.UNAUTHORIZED)
        
        except Exception as e:
            self.response_data = str(e)
            return HttpResponse(self.response_data, status=status.BAD_REQUEST)
        
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        self.response_data['message'] = str(exception)
        return HttpResponse(self.response_data, status=status.BAD_REQUEST)


