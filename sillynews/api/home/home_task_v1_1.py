from .home_task_v1 import HomeTaskV1
from api.decorators.validators import allowed_methods
from helpers.task_helper import TaskHelper
from users.models import UserProfile
from constants import INVALID_RESOURCE
from django.utils import timezone
from home.models import Schedule, Task
from constants import TASK_STATUSES
from django.db.models import Count, Avg, Sum, Q


class HomeTaskV1_1(HomeTaskV1):
    __versions_compatible__ = ('1.1', )
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
                for schedule in schedules:
                    # has_more, tasks = TaskHelper.get_scheduled_task(schedule_id=schedule['id'])
                    schedule['comp_perc'] = comp_perc.get(schedule['id']) if comp_perc.get(schedule['id'], 0) > 0 else 0
                    # schedule['task_list'] = tasks

                items.append({
                    "type": "schedules",
                    "schedules": schedules,
                    "has_more": has_more_schedules,
                })

        data['items'] = items
        # data['has_more'] = has_more
        return data

