from django.urls import path,include
from core import views
from comment import views as comment_views

app_name = 'core'

urlpatterns = [
  path('', views.home, name="home"),
  path('search/', views.search, name='search_results'),
  path('create-content/', views.create_content, name="create_content"),
  path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
  path('video/<slug:video_slug>/', views.DetailView.as_view(), name="video_detail"),
  path('edit-content/<slug:video_slug>/<int:video_id>/', views.edit_content, name="edit_content"),
  path('<slug:video_slug>/<int:video_id>/delete/', views.delete_content, name="delete_content"),
  path('catagory-list/', views.catagory_list, name="catagory_list"),
  path('catagory/<catagory_name>/', views.catagory_detail, name="catagory_detail"),
  path('edit-comment/<int:video_id>/<int:comment_id>/', comment_views.edit_comment, name='edit_comment'),
]
