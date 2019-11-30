from django.contrib.auth.models import User
from django.conf import settings
from django.db import IntegrityError
from users.models import UserProfile
from .firebase import verify_token
from django.utils import timezone
import jwt


class FirebaseAuthBackend:

    def authenticate(self, token):
        firebase_user = verify_token(token)
        if not firebase_user:
            return None
        try:
            profile = UserProfile.objects.get(firebase_uid=firebase_user['uid'])
            if firebase_user.get('email'):
                profile.email = firebase_user.get('email')
                profile.username = firebase_user.get('email')
            if firebase_user.get('phone_number'):
                profile.phone = firebase_user.get('phone_number')
                profile.username = firebase_user.get('phone_number')
            if firebase_user.get('name') and not profile.first_name:
                profile.first_name = firebase_user.get('name').split(' ')[0]
                profile.last_name = ' '.join(firebase_user.get('name').split(' ')[1:])
            profile.signedup_on = timezone.now()
            profile.anonymous = False
            profile.firebase_signin_provider = firebase_user['firebase']['sign_in_provider']
            profile.save()
        except UserProfile.DoesNotExist:
            try:
                if firebase_user.get('phone_number'):
                    profile = UserProfile.objects.get(phone=firebase_user.get('phone_number'), firebase_uid__isnull=True)
                    if firebase_user.get('email'):
                        profile.email = firebase_user.get('email')
                    if firebase_user.get('name') and not profile.first_name:
                        profile.first_name = firebase_user.get('name').split(' ')[0]
                        profile.last_name = ' '.join(firebase_user.get('name').split(' ')[1:])
                elif firebase_user.get('email'):
                    profile = UserProfile.objects.get(email=firebase_user.get('email'), firebase_uid__isnull=True)
                    if firebase_user.get('phone_number'):
                        profile.phone = firebase_user.get('phone_number')
                else:
                    raise UserProfile.DoesNotExist
                profile.firebase_uid = firebase_user['uid']
            except UserProfile.DoesNotExist:
                # username = firebase_user.get('phone_number') or firebase_user.get('email') or firebase_user['uid']
                profile = UserProfile(firebase_uid=firebase_user['uid'],
                                      phone=firebase_user.get('phone_number'))
                if firebase_user.get('email'):
                    profile.email = firebase_user.get('email')
                if firebase_user.get('name') and not profile.first_name:
                    profile.first_name = firebase_user.get('name').split(' ')[0]
                    profile.last_name = ' '.join(firebase_user.get('name').split(' ')[1:])
            profile.firebase_signin_provider = firebase_user['firebase']['sign_in_provider']
            try:
                profile.save()
            except IntegrityError:
                profile = UserProfile.objects.get(firebase_uid=firebase_user['uid'])
        return profile

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user


class JWTAuthBackend:

    def authenticate(self, jwt_token):
        return self._verify_jwt_token(jwt_token)

    def _verify_jwt_token(self, token):
        if not token:
            return None
        profile = None
        try:
            jwt_dict = jwt.decode(token, settings.JWT_KEY)
            profile = UserProfile.objects.get(id=jwt_dict['user_id'])
        except jwt.exceptions.InvalidSignatureError:
            return profile
        except jwt.exceptions.InvalidTokenError:
            return profile
        except UserProfile.DoesNotExist:
            return profile
        return profile

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user