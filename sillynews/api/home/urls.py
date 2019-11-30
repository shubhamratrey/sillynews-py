from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt
from api.decorators import login_required

from . import HomeV1, TaskHomeV1

urlpatterns = [
    re_path('^all/$', HomeV1.as_versioned_view()),
    re_path('^task/$', csrf_exempt(login_required(TaskHomeV1.as_versioned_view()))),
]
