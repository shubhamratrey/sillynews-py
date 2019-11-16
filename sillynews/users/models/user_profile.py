import jwt
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class UserProfile(User):
    """
    UserProfile is the extension of AbstractUser to add ZoopZam based functionality to auth.User
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender')
    )

    phone = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, default=None)
    firebase_uid = models.CharField(max_length=50, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    signedup_on = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(null=True, default=None)
    status = models.CharField(max_length=250, blank=True)
    anonymous = models.BooleanField(default=False)
    avatar = models.CharField(max_length=250, blank=True, null=True)
    firebase_signin_provider = models.CharField(max_length=25, null=True)

    def get_user_doc(self):
        return {
            'id': self.id,
            'name': ' '.join([self.first_name, self.last_name]).strip(),
            'original_avatar': self.avatar if self.avatar else None,
        }

    def get_jwt_token(self):
        return jwt.encode({'user_id': self.id}, settings.JWT_KEY, algorithm='HS512')

    def is_cms_admin(self):
        return self.is_superuser