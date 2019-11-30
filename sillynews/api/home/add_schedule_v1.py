from dateutil import parser
from api.responses.base import APIResponseBase
from api.decorators.validators import allowed_methods
from constants import INVALID_RESOURCE, DAYS_OF_WEEK
from home.models import Schedule


class AddScheduleV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')

    def __init__(self, **kwargs):
        super(AddScheduleV1, self).__init__(**kwargs)
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

        start_time = request.POST.get('start_time')
        if not start_time:
            self.set_bad_req('Start time can not be empty.', INVALID_RESOURCE.TIME)
            return data
        end_time = request.POST.get('end_time')
        if not end_time:
            self.set_bad_req('End time can not be empty.', INVALID_RESOURCE.TIME)
            return data
        try:
            start_time = parser.parse(start_time)
            end_time = parser.parse(end_time)
        except:
            self.set_bad_req('Invalid time.', '')
            return data

        day = request.POST.get('day')
        if day and day not in DAYS_OF_WEEK.ALL_DAY:
            self.set_bad_req('Invalid day.', INVALID_RESOURCE.DAY)
            return data

        schedule = Schedule.objects.create(title=title, profile=profile, start_time=start_time, end_time=end_time,
                                           days=day)
        data['schedule'] = schedule.to_json()
        return data
