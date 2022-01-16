from django.urls import path
from account import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
     path('signup/', views.signup, name="signup"),
     # authentication
     path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
     path('profile/<int:profile_id>/', views.profile, name="profile"),
     path('update-profile/<int:profile_id>/', views.update_profile, name="update_profile"),
     # follow
     path('follow/', views.follow, name="follow"),
     # like
     path('like/', views.like, name="like"),
     # dislike
     path('dislike/', views.dislike, name="dislike"),
     # upvote comment
     path('upvote/', views.upvote, name="upvote"),
     # downvote comment
     path('downvote/', views.downvote, name="downvote"),
     # Add catagory to favourite
     path('add-favourite/<int:catagory_id>/', views.add_favourite, name="add_favourite"),
      # following_list
     path('following_list/', views.following_list, name="following_list"),

]
