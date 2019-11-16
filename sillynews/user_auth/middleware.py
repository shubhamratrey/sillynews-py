from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import authenticate


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        authorization = request.META.get('HTTP_AUTHORIZATION', '').split(' ')
        if len(authorization) > 1:
            token = authorization[1]
            if authorization[0] == 'Bearer':
                user = authenticate(token=token)
                if user:
                    request.user = user
            elif authorization[0] == 'jwt':
                user = authenticate(jwt_token=token)
                if user:
                    request.user = user
        else:
            jwt_token = request.POST.get('token')
            user = authenticate(jwt_token=jwt_token)
            if user:
                request.user = user
