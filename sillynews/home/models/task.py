from django.db import models
import uuid
from django.utils.text import slugify
import constants


class Schedule(models.Model):
    profile = models.ForeignKey('users.UserProfile', null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    icon_url = models.CharField(max_length=512, null=True)
    status = models.CharField(choices=constants.SCHEDULE_STATUSES.VALID_STATUSES,
                              default=constants.SCHEDULE_STATUSES.ACTIVE, max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    days = models.CharField(max_length=255, choices=constants.DAYS_OF_WEEK.VALID_DAYS,
                            default=constants.DAYS_OF_WEEK.VALID_DAYS)

    def to_json(self):
        doc = {
            'id': self.id,
            'title': self.title,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'slug': self.slug,
            'icon_url': self.icon_url,
        }
        return doc

    def _get_unique_slug(self):
        slug = slugify(self.title) or str(uuid.uuid4())
        unique_slug = slug
        num = 1
        while Schedule.objects.filter(slug=unique_slug, profile_id=self.profile_id).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Schedule, self).save(*args, **kwargs)


class Task(models.Model):
    schedule = models.ForeignKey('home.Schedule', null=True, on_delete=models.CASCADE)
    profile = models.ForeignKey('users.UserProfile', null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    added_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=constants.TASK_STATUSES.VALID_STATUSES,
                              default=constants.TASK_STATUSES.PENDING, max_length=255, db_index=True)
    rank = models.IntegerField(null=True)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status,
        }