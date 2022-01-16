from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Catagory,Video
from account.models import Profile,Follow
from django.contrib.auth.models import User
import subprocess
from PIL import Image
from moviepy.editor import *
# comments
from comment.models import Comment
from comment.forms import CommentForm

from core.forms import ContentCreateForm

from django.db.models import Q

from django.template.defaultfilters import slugify

from django.views.generic.edit import DeleteView

from hitcount.views import HitCountDetailView

from django.contrib.auth.decorators import login_required

from itertools import chain

from django.core.exceptions import PermissionDenied


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        # video_list = []
        # cat_list = Catagory.objects.filter(favourite=request.user)
        # following_list = Follow.objects.filter(follower=request.user)
        # follower_videos = Video.objects.filter(user__in=following_list.values_list('following')).order_by('-hit_count_generic__hits')[0:5]
        # fav_cat_list = Video.objects.filter(catagory__in=cat_list.values_list('videos')).order_by('-hit_count_generic__hits')
        # popular_list = Video.objects.exclude(title__in=fav_cat_list.values_list('title')).order_by('-hit_count_generic__hits')
        # video_list = list(chain(follower_videos,fav_cat_list, popular_list))
        # video_list = list(dict.fromkeys(video_list))
        video_list = Video.objects.all().order_by('-hit_count_generic__hits')
        print(video_list)
    else:
        print(request.user)
        video_list = Video.objects.all().order_by('-hit_count_generic__hits')
    context = {
       'video_list': video_list,
    }
    return render(request,'core/home.html',context=context)

class DetailView(HitCountDetailView):
    model = Video        # your model goes here
    count_hit = True    # set to True if you want it to try and count the hit

    def get_object(self):
        video = Video.objects.get(slug=self.kwargs.get('video_slug'))
        return video

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        video = self.get_object()
        print(video)
        catagory = video.catagory.id
        related_videos = Video.objects.filter(catagory=catagory).exclude(slug=video.slug)
        comments = video.comments.all()
        # comments = video.comments.filter(status=True)
        comment_form = CommentForm()
        user = User.objects.get(id=video.user.id)
        profile = get_object_or_404(Profile, user=user)
        if self.request.user.is_authenticated:
            following_list = Follow.objects.filter(follower=self.request.user)
            following_channel_list = following_list.values_list('following', flat=True)
        else:
            following_channel_list = None
        follower_count = user.follower.count()
        context['video'] = video
        context['comments'] = comments
        context['comment_form'] = comment_form
        context['follower_count'] = follower_count
        context['related_videos'] = related_videos
        context['profile'] = profile
        context['following_channel_list'] = following_channel_list
        return context




# def video_detail(request,video_slug, video_id):
#     video = get_object_or_404(Video, id=video_id)
#     catagory = video.catagory.id
#     related_videos = Video.objects.filter(catagory=catagory)
#     print(related_videos)
#     comments = video.comments.filter(status=True)
#     comment_form = CommentForm()
#     user = User.objects.get(id=video.user.id)
#     print(user)
#     follower_count = user.follower.count()
#     print(follower_count)
#     print(comment_form)
#     context = {
#     'video': video,
#     'comments': comments,
#     'comment_form': comment_form,
#     'follower_count': follower_count,
#     'related_videos': related_videos,
#     }
#     return render(request, 'core/video_detail.html',context)
@login_required
def search(request):
     query = request.GET.get('q')
     mark = bool
     videos = []
     following_channel_list = ''
     if query:
         profiles = Profile.objects.filter(
                                           Q(channel_name__iexact = query)|
                                           Q(channel_name__icontains = query))
         print(profiles)
         following_list = Follow.objects.filter(follower=request.user)
         print(following_list)
         search_videos = Video.objects.filter(
                                   Q(title__icontains = query) |
                                   Q(catagory__name__icontains = query) |
                                   Q(user__username__icontains = query)).order_by('like_count')
         # posts = list(dict.fromkeys(posts))
         # posts_count = len(posts)
         if profiles:
             following_channel_list = following_list.values_list('following', flat=True)
             print(following_channel_list)
     else:
         query = ""
         search_videos = None
         profiles = None
         following_channel_list = None
     context = {
       'query': query,
       'search_videos': search_videos,
       'profiles': profiles,
       'following_channel_list': following_channel_list,
       # 'posts_count': posts_count,
       'mark': mark,
     }
     return render(request, 'core/search_results.html', context=context)


def catagory_list(request):
    catagory_list = Catagory.objects.all().order_by('name')
    if request.user.is_authenticated:
        fav_cat_list = Catagory.objects.filter(favourite=request.user)
    else:
        fav_cat_list = None
    # fav_cat_list = fav_cat.values_list('favourite', flat=True)

    for catagory in catagory_list:
        videos = Video.objects.filter(catagory=catagory)
        videos_count = videos.count()
        catagory.videos_count = videos_count
        print(catagory)
        print(catagory.videos_count)

    context = {
    'catagory_list': catagory_list,
    'fav_cat_list': fav_cat_list,
    }
    return render(request,'core/catagory_list.html',context=context)

def catagory_detail(request,catagory_name):
    catagory = Catagory.objects.get(name=catagory_name)
    videos_list = Video.objects.filter(catagory=catagory)
    print(videos_list)
    context = {
     'catagory': catagory,
     'videos_list': videos_list,
    }
    return render(request,'core/catagory_detail.html',context=context)

@login_required
def create_content(request):
    if request.method == 'POST':
        form = ContentCreateForm(request.POST,request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            # video_title = video.cleaned_data.get('title')
            # slug = slugify(video_title)
            video.save()
            return redirect('core:video_detail',video_slug=video.slug)
    else:
        form = ContentCreateForm()
    context = {
    'form': form,
    }
    return render(request,'core/content_create_form.html',context=context)

@login_required
def edit_content(request,video_slug,video_id):
    video = Video.objects.get(id=video_id)
    edit_content_page = True
    if request.user == video.user:
        if request.method == 'POST':
            form = ContentCreateForm(request.POST,request.FILES,instance=video)
            if form.is_valid():
                form.save()
                return redirect('core:video_detail',video_slug=video.slug)
        else:
            form = ContentCreateForm(instance=video)
    else:
        raise PermissionDenied()
    context = {
        'form': form,
        'edit_content_page': edit_content_page,
    }
    return render(request,'core/content_create_form.html',context=context)

@login_required
def delete_content(request, video_slug, video_id):
    video  = get_object_or_404(Video,id=video_id)
    profile = get_object_or_404(Profile,user=video.user)
    if request.user == video.user:
        if request.method == 'POST':
            video.delete()
            return redirect('account:profile', profile_id=profile.id)
    else:
        raise PermissionDenied()
    context = {
     'video': video,
    }
    return render(request,'core/video_confirm_delete.html', context=context)
