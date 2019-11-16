import json
from functools import wraps

from django.http import HttpResponse
from django.utils.decorators import available_attrs


def login_required(function):
    @wraps(function, assigned=available_attrs(function))
    def wrapped_function(request, *args, **kwargs):
        user = request.user
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)

        if request.path.startswith('/api/'):
            return HttpResponse(json.dumps({
                'status': 'error',
                'status_code': 401,
                'message': 'Login required to access this resource'}),
                content_type='application/json',
                status=401)

    return wrapped_function
