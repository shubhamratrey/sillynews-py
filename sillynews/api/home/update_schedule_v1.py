from dateutil import parser
from api.responses.base import APIResponseBase
from api.decorators.validators import allowed_methods
from constants import INVALID_RESOURCE, SCHEDULE_STATUSES, DAYS_OF_WEEK
from home.models import Schedule


class UpdateScheduleV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')

    def __init__(self, **kwargs):
        super(UpdateScheduleV1, self).__init__(**kwargs)
        self.allowed_methods = ('POST', 'DELETE')

    @allowed_methods
    def get_or_create_data(self):
        data = {}
        profile = self.get_profile()
        if profile.is_anonymous:
            self.set_403()
            return data
        schedule_id = self.kwargs.get('schedule_id')
        try:
            schedule = Schedule.objects.get(pk=schedule_id)
        except Schedule.DoesNotExist:
            self.set_404("Invalid schedule.", INVALID_RESOURCE.SCHEDULE)
            return data

        request = self.get_request()
        if request.method == 'DELETE':
            schedule.status = SCHEDULE_STATUSES.DELETED
            schedule.save()
        elif request.method == 'POST':
            title = request.POST.get('title')
            if title:
                schedule.title = title
            start_time = request.POST.get('start_time')
            if start_time:
                try:
                    start_time = parser.parse(start_time)
                    schedule.start_time = start_time
                except:
                    self.set_bad_req('Invalid time.', '')
                    return data
            end_time = request.POST.get('start_time')
            if end_time:
                try:
                    end_time = parser.parse(end_time)
                    schedule.end_time = end_time
                except:
                    self.set_bad_req('Invalid time.', '')
                    return data
            day = request.POST.get('day')
            if day and day in DAYS_OF_WEEK.ALL_DAY:
                schedule.days = day
            schedule.save()

        data['schedule'] = schedule.to_json()
        return data
