from django.db import models
import uuid
from django.utils.text import slugify


class NewsRssLink(models.Model):
    content_type = models.ForeignKey('home.ContentType', on_delete=models.CASCADE)
    link = models.CharField(max_length=512, null=False)
    title = models.CharField(max_length=255, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    link_rank = models.IntegerField(null=True, db_index=True)

    def to_json(self):
        doc = {
            'id': self.id,
            'link': self.link,
            'image': self.image,
            'content_type': self.content_type,
        }
        return doc


class NewsContentType(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    icon_url = models.CharField(max_length=512, null=True)
    is_active = models.BooleanField(default=False, db_index=True)
    rank = models.IntegerField(null=True)

    def _get_unique_slug(self):
        slug = slugify(self.title) or str(uuid.uuid4())
        unique_slug = slug
        num = 1
        while NewsContentType.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(NewsContentType, self).save(*args, **kwargs)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'uri': self.get_uri()
        }

    def get_uri(self):
        return 'app://app/content-types/%s' % self.slug


class NewsChannel(models.Model):
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(null=True)
    icon_url = models.CharField(max_length=512, null=True)
