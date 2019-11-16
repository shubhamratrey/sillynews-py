import uuid
import datetime
from decimal import Decimal
from django.conf import settings
from pytz import timezone
from django.utils import timezone as django_timezone


class UtilsHelper(object):
    @staticmethod
    def replace_timezone_to_ist(time):
        if type(time) != datetime.datetime:
            return time
        ist_timezone = timezone('Asia/Kolkata')
        time = time.replace(tzinfo=ist_timezone)
        return time

    @staticmethod
    def get_today_ist():
        now = django_timezone.now()
        now_ist = UtilsHelper.replace_timezone_to_ist(now)
        today_start = now_ist.replace(hour=0, minute=0, second=0, microsecond=0)
        return today_start

    @staticmethod
    def get_random_uuid():
        return uuid.uuid4().hex

    @staticmethod
    def is_prod():
        env = getattr(settings, 'ENV', 'dev')
        return env in ('prod', 'preprod')

    @staticmethod
    def replace_decimals(obj):
        if isinstance(obj, list):
            for i in range(len(obj)):
                obj[i] = UtilsHelper.replace_decimals(obj[i])
            return obj
        elif isinstance(obj, dict):
            for k in obj.keys():
                obj[k] = UtilsHelper.replace_decimals(obj[k])
            return obj
        elif isinstance(obj, set):
            new_set = set()
            for i, j in enumerate(obj):
                new_set.add(UtilsHelper.replace_decimals(j))
            return new_set
        elif isinstance(obj, Decimal):
            if obj % 1 == 0:
                return int(obj)
            else:
                return float(obj)
        else:
            return obj
