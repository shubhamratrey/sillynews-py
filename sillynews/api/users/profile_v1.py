from api.responses.base import APIResponseBase
from api.decorators.validators import allowed_methods
from users.models import UserProfile
from constants.error_codes import INVALID_RESOURCE


class ProfileV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')
    __page_size__ = 10

    def __init__(self, **kwargs):
        super(ProfileV1, self).__init__(**kwargs)
        self.allowed_methods = ('GET',)

    @allowed_methods
    def get_or_create_data(self):
        data = {}
        profile = self.get_profile()
        user_id = self.kwargs.get('user_id')
        if not profile and not user_id:
            self.set_404('Invalid User Page.', INVALID_RESOURCE.USER_ID)
            return data

        is_self = False
        if profile and (not user_id or profile.id == int(user_id)):
            is_self = True
            user_id = profile.id

        if is_self:
            user = profile
        else:
            try:
                user = UserProfile.objects.get(pk=user_id)
            except UserProfile.DoesNotExist:
                self.set_404('User Not Found.', INVALID_RESOURCE.USER_ID)
                return data

        data['user'] = user.get_user_doc()
        if is_self:
            data['user']['email'] = user.email
            data['user']['phone'] = user.phone
            data['user']['is_cms_admin'] = profile.is_cms_admin()
            sign_up_source = {'google.com': 'email', 'phone': 'phone'}
            data['user']['sign_up_source'] = sign_up_source.get(user.firebase_signin_provider, '')
            data['user']['is_self'] = is_self

        return data
