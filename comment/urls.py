from django.urls import path
from comment import views
app_name = 'comment'

urlpatterns = [
      # add comment
      path('post-comment/<int:video_id>/', views.post_comment, name='post_comment'),
         # Added code to handle secondary replies
      path('post-comment/<int:video_id>/<int:parent_comment_id>/', views.post_comment, name='comment_reply'),
        # edit comment
       # delete comment
      path('<slug:slug>/<int:comment_id>/', views.delete_comment, name="delete_comment"),
]
