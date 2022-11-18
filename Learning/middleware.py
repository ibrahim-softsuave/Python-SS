from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse
from Learning import excluded_endpoints
from http import HTTPStatus as status
from rest_framework_simplejwt import exceptions


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION')
        try:
            if request.path not in excluded_endpoints:
                if not access_token:
                    return HttpResponse('Token Required', status=status.BAD_REQUEST)
                jwt_auth = JWTAuthentication()
                user, payload = jwt_auth.authenticate(request)
                request.payload = payload.payload
        
        except exceptions.InvalidToken as e:
            return HttpResponse("Invalid Token or Token got expired", status=status.UNAUTHORIZED)
        
        except Exception as e:
            return HttpResponse(str(e), status=status.BAD_REQUEST)
        
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        return HttpResponse(str(exception), status=status.BAD_REQUEST)


