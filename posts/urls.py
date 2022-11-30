from django.urls import path
from .views import PostView,PostListView,LikeView,FileListView,FileDetailView



urlpatterns=[
    path('post/',PostView.as_view(),name='post'),
    path('post/<int:post_pk>/',PostView.as_view(),name='post'),
    path('post-list/',PostListView.as_view(),name='post-list'),
    path('post/<int:post_pk>/likes/',LikeView.as_view(),name='like'),
    path('post/<int:post_pk>/files',FileListView.as_view(),name='file-list'),
    path('post/<int:post_pk>/files/<int:pk>/',FileDetailView.as_view(),name='file-detail'),

]