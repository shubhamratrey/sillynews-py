from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt
from api.decorators import login_required

from .profile_v1 import ProfileV1
from . import UpdateProfileV1

urlpatterns = [
    re_path('^me/$', csrf_exempt(login_required(ProfileV1.as_versioned_view()))),
    re_path('^me/update/$', csrf_exempt(login_required(UpdateProfileV1.as_versioned_view()))),
    re_path('^(?P<user_id>\d+)/$', ProfileV1.as_versioned_view()),
]
