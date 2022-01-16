from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import CreateView
from .forms import SignupForm,UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from .models import Profile,Follow
from django.contrib.auth.models import User
from core.models import Catagory,Video
from comment.models import Comment
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            obj,created = Profile.objects.get_or_create(user=user, channel_name=user.username)
            messages.success(request, f'Your account has been created successfully!You are now able to login')
            return redirect('account:login')
    else:
        form = SignupForm()
    context = {
      'form': form
    }
    return render(request,'account/signup.html',context=context)

def profile(request,profile_id):
    # user =  User.objects.get(username=username)
    profile = get_object_or_404(Profile,id=profile_id)
    # profile = get_object_or_404(Profile,channel_name=channel_name)
    print(profile)
    video_list = Video.objects.filter(user=profile.user).order_by('created')
    context = {
    'profile': profile,
    'video_list': video_list,
    }
    return render(request,'account/profile.html',context=context)

@login_required
def update_profile(request,profile_id):
    # user =  User.objects.get(username=username)
    profile = get_object_or_404(Profile, id=profile_id)
    if request.user == profile.user:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST,instance=request.user)
            p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=profile,)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request,f'Your profile has been updated!')
                return redirect('account:profile',profile_id=profile_id)
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=profile)
    else:
        raise PermissionDenied()
        HttpResponse("You are denied to access this page.")
    context = {
      'u_form': u_form,
      'p_form': p_form,
    }
    return render(request, 'account/edit_profile.html',context=context)

@csrf_exempt
def follow(request):
    if request.POST.get('action') == 'post':
        result = ''
        user_id = int(request.POST.get('video_user'))
        following_user = User.objects.get(id=user_id)
        print(following_user)
        allready_followed = Follow.objects.filter(following=following_user,follower=request.user)
        print(allready_followed)
        follower_count = following_user.follower.count()
        if allready_followed:
            allready_followed.delete()
            follower_count -= 1
            result = follower_count
            print(result)
        else:
            follow = Follow.objects.create(following=following_user,follower=request.user)
            follower_count += 1
            result = follower_count
            follow.save()
        return JsonResponse({'result': result })


@login_required
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('videoid'))
        video = get_object_or_404(Video, id=id)
        if video.like.filter(id=request.user.id).exists():
            video.like.remove(request.user)
            video.like_count -= 1
            result = video.like_count
            video.save()
        else:
            video.like.add(request.user)
            video.like_count += 1
            result = video.like_count
            video.save()
        return JsonResponse({'result': result })

@login_required
def dislike(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('videoid'))
        video = get_object_or_404(Video, id=id)
        if video.dislike.filter(id=request.user.id).exists():
            video.dislike.remove(request.user)
            video.dislike_count -= 1
            result = video.dislike_count
            video.save()
        else:
            video.dislike.add(request.user)
            video.dislike_count += 1
            result = video.dislike_count
            video.save()
        return JsonResponse({'result': result })

@login_required
def upvote(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('commentid'))
        comment = get_object_or_404(Comment, id=id)
        print(comment)
        if comment.upvote.filter(id=request.user.id).exists():
            comment.upvote.remove(request.user)
            comment.upvote_count -= 1
            result = comment.upvote_count
            print(result)
            comment.save()
        else:
            comment.upvote.add(request.user)
            comment.upvote_count += 1
            result = comment.upvote_count
            print(result)
            comment.save()
        return JsonResponse({'result': result })

@login_required
def downvote(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('commentid'))
        comment = get_object_or_404(Comment, id=id)
        print(comment)
        print(comment.downvote)
        if comment.downvote.filter(id=request.user.id).exists():
            comment.downvote.remove(request.user)
            comment.downvote_count -= 1
            result = comment.downvote_count
            print(result)
            comment.save()
        else:
            comment.downvote.add(request.user)
            comment.downvote_count += 1
            result = comment.downvote_count
            comment.save()
        return JsonResponse({'result': result })

@login_required
def add_favourite(request,catagory_id):
    catagory = get_object_or_404(Catagory, id=catagory_id)
    if catagory.favourite.filter(id = request.user.id).exists():
        catagory.favourite.remove(request.user)
        messages.success(request, f'Catagory removed from your favourite list')
    else:
        catagory.favourite.add(request.user)
        messages.success(request, f'Catagory added to your favourite list')
    return HttpResponseRedirect(reverse('core:catagory_list'))
    # return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def following_list(request):
    following_list = Follow.objects.filter(follower=request.user)
    print(following_list)
    context = {
     'following_list': following_list,
    }
    return render(request,'account/following_list.html',context=context)
