from django.db import models
from django.contrib.auth.models import User
from core.models import Video
from django.urls import reverse

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,
                               on_delete=models.CASCADE,
                               related_name='user_profile')
    profile_pic = ProcessedImageField(default="default_profile_image.jpg", upload_to='profile_pic',
                                           null=True, blank=True,
                                           processors=[ResizeToFill(200, 200)],
                                           format='JPEG',
                                           options={'quality': 75})
    channel_name = models.CharField(default='', max_length=264, blank=True)
    description = models.TextField(default='', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    website = models.URLField(blank=True,null=True)


    def __str__(self):
        return self.user.username

    @property
    def total_videos(self):
        videos = Video.objects.filter(user=self.user)
        videos_count = videos.count()
        return videos_count

    @property
    def videos(self):
        videos = Video.objects.filter(user=self.user).order_by('like_count')
        return videos

    # def get_absolute_url(self):
    #     return reverse('post_detail', args=[str(self.user.username)])
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,related_name="following")
    follower_count = models.IntegerField(default='0')
    following_count = models.IntegerField(default='0')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.follower.username + ' follows ' + self.following.username
