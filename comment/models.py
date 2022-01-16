from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from core.models import Video
from django.contrib.auth.models import User
# Create your models here.
class Comment(MPTTModel):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name = 'comments')
    parent = TreeForeignKey('self',on_delete=models.SET_NULL,
                            null=True,
                            blank=True,
                            related_name='children')
    reply_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='replayers')
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    content = models.TextField()
    upvote = models.ManyToManyField(User, related_name="upvoter", default=None, blank=True)
    upvote_count = models.IntegerField(default='0')
    downvote =  models.ManyToManyField(User, related_name="downvoter", default=None, blank=True)
    downvote_count = models.IntegerField(default='0')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return  f'{self.content[:20]} by {self.user}'
