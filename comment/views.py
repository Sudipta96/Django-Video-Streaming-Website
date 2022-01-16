from django.shortcuts import render,get_object_or_404,redirect,reverse
from .forms import CommentForm,CommentUpdateForm
from core.models import Video
from .models import Comment
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required
@csrf_exempt
def  post_comment( request , video_id , parent_comment_id = None ):
    video  =  get_object_or_404(Video,id=video_id )
    print('this is post_slug')
    # Processing POST request
    if  request.method == 'POST' :
        comment_form  =  CommentForm(request.POST)
        if  comment_form.is_valid ():
            new_comment  =  comment_form.save(commit = False )
            new_comment.video =  video
            new_comment.user =  request.user
            video_slug = video.slug
            print(new_comment.user)
            child = bool

            # Secondary reply
            if  parent_comment_id:
                parent_comment  =  Comment.objects.get(id=parent_comment_id)
                # If the reply level exceeds the second level, it will be converted to the second level
                new_comment.parent_id = parent_comment.get_root().id

                # Respondent
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                print(new_comment)
                # super_parent = Comment.objects.get(id = parent_comment.get_root().id)
                # print(super_parent.get_children().count())
                # if super_parent.get_children().count() > 1:
                #     child = True
                return HttpResponse("200 OK")
            new_comment.save()
            return redirect('core:video_detail',video_slug=video_slug)
        else :
            return HttpResponse( "The content of the form is incorrect, please fill in again.")
    # Processing GET request
    elif request.method  ==  'GET':
        comment_form  =  CommentForm()
        context  = {
            'comment_form' : comment_form ,
            'video_id' : video_id ,
            'parent_comment_id' : parent_comment_id
        }
        return  render(request, 'comment/reply.html', context)
    # Processing other requests
    else :
        return  HttpResponse( "Only accept GET/POST requests.")

@login_required
@csrf_exempt
def edit_comment(request, video_id, comment_id):
    # video  =  get_object_or_404 (Video, id=video_id)
    comment = Comment.objects.get(id=comment_id)
    print(comment)
    if request.method == 'POST':
        edit_form = CommentUpdateForm(request.POST,instance=comment)
        print(edit_form)
        if edit_form.is_valid():
            edit_form.status = False
            edit_form.save()
            messages.success(request, f'Your comment has been updated!')
            return HttpResponse('Updating...')
            # return redirect('post_detail',slug=post.slug)
        else:
            return HttpResponse("The content of the form is incorrect, please fill in again.")
    else:
        edit_form = CommentUpdateForm(instance=comment)
        print(edit_form)
    context = {
    'edit_form': edit_form,
    'video_id' : video_id,
    'comment_id': comment_id,
    }
    return render(request,'comment/edit_comment.html',context=context)

@login_required
def delete_comment(request, slug, comment_id):
    video = get_object_or_404(Video,slug=slug)
    print(video)
    comment  = Comment.objects.get(id=comment_id).delete()
    messages.success(request, f'Your comment has been deleted!')
    return HttpResponseRedirect(reverse('core:video_detail',kwargs={'video_slug':slug}))
