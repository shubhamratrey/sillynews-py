from api.responses.base import APIResponseBase
from api.decorators.validators import allowed_methods
from constants import INVALID_RESOURCE
from home.models import Task


class AddTaskV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')

    def __init__(self, **kwargs):
        super(AddTaskV1, self).__init__(**kwargs)
        self.allowed_methods = ('POST',)

    @allowed_methods
    def get_or_create_data(self):
        data = {}
        profile = self.get_profile()
        if profile.is_anonymous:
            self.set_403()
            return data

        request = self.get_request()
        title = request.POST.get('title')
        if not title:
            self.set_bad_req('Title not provided', INVALID_RESOURCE.TITLE)
            return data

        schedule_id = request.POST.get('schedule_id')
        if not schedule_id:
            self.set_bad_req('Schedule not provided', INVALID_RESOURCE.SCHEDULE)
            return data

        rank = 1
        try:
            _task = Task.objects.filter(profile_id=profile.id).latest('rank')
        except Task.DoesNotExist:
            pass
        else:
            if _task.rank:
                rank = _task.rank + 1

        task = Task.objects.create(title=title, schedule_id=schedule_id, profile_id=profile.id, rank=rank)
        data['task'] = task.to_json()
        if task.schedule:
            data['task']['schedule'] = task.schedule.to_json()

        return data
