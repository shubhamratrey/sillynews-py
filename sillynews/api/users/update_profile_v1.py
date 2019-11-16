from api.responses.base import APIResponseBase
from api.decorators.validators import allowed_methods
from constants import INVALID_RESOURCE


class UpdateProfileV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')

    def __init__(self, **kwargs):
        super(UpdateProfileV1, self).__init__(**kwargs)
        self.allowed_methods = ('POST', )

    @allowed_methods
    def get_or_create_data(self):
        data = {}
        profile = self.get_profile()
        if profile.is_anonymous:
            self.set_403()
            return data
        user_id = self.get_sanitized_int(self.kwargs.get('user_id'))
        if user_id and profile.id != user_id:
            self.set_403()
            return data

        request = self.get_request()
        name = request.POST.get('name', '')
        if name:
            first_name = name.split(' ')[0]
            if len(first_name) >= 30:
                self.set_bad_req('Name too big.', INVALID_RESOURCE.NAME)
                return data
            profile.first_name = first_name
            if len(name.split(' ')) > 0:
                last_name = ' '.join(name.split(' ')[1:])
                if len(last_name) >= 150:
                    self.set_bad_req('Name too big.', INVALID_RESOURCE.NAME)
                    return data
                profile.last_name = last_name

        profile.save()

        data['user'] = profile.get_user_doc()

        return data
