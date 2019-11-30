from api.responses.base import APIResponseBase
from api.decorators.validators import allowed_methods
from constants import INVALID_RESOURCE, TASK_STATUSES
from home.models import Task


class UpdateTaskV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')

    def __init__(self, **kwargs):
        super(UpdateTaskV1, self).__init__(**kwargs)
        self.allowed_methods = ('POST',)

    @allowed_methods
    def get_or_create_data(self):
        data = {}
        profile = self.get_profile()
        if profile.is_anonymous:
            self.set_403()
            return data
        task_id = self.kwargs.get('task_id')
        try:
            _task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            self.set_404("Invalid task.", INVALID_RESOURCE.TASK)
            return data

        request = self.get_request()
        if request.method == 'DELETE':
            _task.status = TASK_STATUSES.DELETED
            _task.save()
        elif request.method == 'POST':
            title = request.POST.get('title')
            if title:
                _task.title = title
            status = request.POST.get('status')
            if status and status in (TASK_STATUSES.COMPLETED, TASK_STATUSES.PENDING):
                _task.status = status
            schedule_id = request.POST.get('schedule_id')
            if schedule_id:
                _task.schedule_id = schedule_id
            _task.save()

        data['task'] = _task.to_json()
        if _task.schedule:
            data['task']['schedule'] = _task.to_json()
        return data
