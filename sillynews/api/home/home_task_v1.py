from api.responses.base import APIResponseBase
from api.decorators.validators import allowed_methods
from helpers.task_helper import TaskHelper
from users.models import UserProfile
from constants import INVALID_RESOURCE
from django.utils import timezone


class HomeTaskV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')
    __page_size__ = 10

    def __init__(self, **kwargs):
        super(HomeTaskV1, self).__init__(**kwargs)
        self.allowed_methods = ('GET',)

    @allowed_methods
    def get_or_create_data(self):
        data = {}
        items = []
        profile = self.get_profile()
        request = self.get_request()
        page_no = self.get_sanitized_int(self.request.GET.get('page', 1))
        page_size = self.get_sanitized_int(self.request.GET.get('page_size', self.__page_size__))
        _type = request.GET.get('type')
        day = request.GET.get('day')
        has_more = False
        if _type == 'schedules':
            has_more_schedules, schedules = TaskHelper.get_schedules(profile_id=profile.id, page_no=page_no,
                                                                     page_size=page_size, day=day)
            has_more = has_more_schedules
            items.append({
                "type": "schedules",
                "schedules": schedules,
                "has_more": has_more_schedules,
            })
        else:
            if page_no == 1:
                try:
                    profile = UserProfile.objects.get(pk=profile.id)
                except UserProfile.DoesNotExist:
                    self.set_404('Invalid profile.', INVALID_RESOURCE.USER_ID)
                    return
                items.append({
                    "type": 'user_info',
                    "user_info": {
                        "name": ' '.join([profile.first_name, profile.last_name]).strip(),
                        "quote": "Quote of the day",
                        "n_pending_task": 4,
                        "n_total_task": 10,
                        "time ": timezone.now().isoformat()
                    }
                })
                has_more_schedules, schedules = TaskHelper.get_schedules(profile_id=profile.id, page_no=page_no,
                                                                         page_size=page_size, day=day)
                schedule_ids = [schedule['id'] for schedule in schedules]
                comp_perc = TaskHelper.get_schedules_comp_perc(schedules_ids=schedule_ids)
                items.append({
                    "type": "schedules",
                    "schedules": schedules,
                    "has_more": has_more_schedules,
                })
            has_more_task, tasks = TaskHelper.get_task(profile_id=profile.id, page_no=page_no, page_size=page_size)
            has_more = has_more_task
            items.append({
                "type": "tasks",
                "tasks": tasks,
                "has_more": has_more_task,
            })
        data['items'] = items
        data['has_more'] = has_more
        return data
