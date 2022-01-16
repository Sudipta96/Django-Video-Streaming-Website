from django.db import models
from django.contrib.auth.models import User
# 287/161
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from .validators import validate_file_extension

from django.utils.text import slugify

from moviepy.editor import *

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericRelation

from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT


# Create your views here.
def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return hours, mins, seconds

class Catagory(models.Model):
    name = models.CharField(max_length=75)
    avatar = ProcessedImageField(default="default_category_avatar.jpg", upload_to='catagory_avatar/%Y/%m/%d/',
                                           null=True, blank=True,
                                           processors=[ResizeToFill(320, 180)],
                                           format='JPEG',
                                           options={'quality': 90})
    favourite = models.ManyToManyField(User, related_name="favourite", default=None, blank=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Video(models.Model, HitCountMixin):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploader")
    file = models.FileField(upload_to="videos/%Y/%m/%d/",validators=[validate_file_extension])
    thumbnail = ProcessedImageField(upload_to='video_thumbnail/%Y/%m/%d/',
                                           processors=[ResizeToFill(300, 180)],
                                           format='JPEG',
                                           options={'quality': 75})
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    catagory = models.ForeignKey(Catagory, on_delete=models.PROTECT, related_name='videos')
    like = models.ManyToManyField(User, related_name="like", default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    dislike = models.ManyToManyField(User, related_name="dislike", default=None, blank=True)
    dislike_count = models.BigIntegerField(default='0')
    hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')


    class Meta:
        ordering = ['catagory']

    def __str__(self):
        return self.user.username +  " Catagory: " + self.catagory.name + " " +  self.title[:30]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super(Video, self).save(*args,**kwargs)

    @property
    def get_duration(self):
        video = VideoFileClip(self.file.path)
        video_duration = int(video.duration)
        hours, mins, secs = convert(video_duration)
        if secs < 10:
            secs = '0' + str(secs)
        if mins < 10:
            mins = '0' + str(mins)
        if hours != 0:
            duration = str(hours) + ":" + str(mins) + ":" + str(secs)
        else:
            duration = str(mins) + ":" + str(secs)
        return duration
