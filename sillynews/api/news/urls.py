from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt
from api.decorators import login_required

from . import NewsListV1

urlpatterns = [
    re_path('^all/$', NewsListV1.as_versioned_view()),
]
