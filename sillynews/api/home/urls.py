from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt
from api.decorators import login_required

from . import HomeV1, HomeTaskV1, AddScheduleV1, AddTaskV1, UpdateTaskV1, UpdateScheduleV1

urlpatterns = [
    re_path('^all/$', HomeV1.as_versioned_view()),
    re_path('^task/$', csrf_exempt(login_required(HomeTaskV1.as_versioned_view()))),
    re_path('^add-task/$', csrf_exempt(login_required(AddTaskV1.as_versioned_view()))),
    re_path('^add-schedule/$', csrf_exempt(login_required(AddScheduleV1.as_versioned_view()))),
    re_path('^(?P<task_id>[\d-]+)/update-task/$', csrf_exempt(login_required(UpdateTaskV1.as_versioned_view()))),
    re_path('^(?P<schedule_id>[\d-]+)/update-schedule/$', csrf_exempt(login_required(UpdateScheduleV1.as_versioned_view()))),
]
