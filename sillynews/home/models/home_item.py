from django.db import models
import constants


class HomeItem(models.Model):
    item_type = models.CharField(choices=constants.HOME_ITEM_TYPES.VALID_TYPES, max_length=32, null=False)
    item_id = models.IntegerField(default=-1, db_index=True)
    sequence_no = models.IntegerField(default=1, db_index=True)
    login_required = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=False, db_index=True)
    home_version = models.IntegerField(default=1, db_index=True)
