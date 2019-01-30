from django.urls import path
from .views import (
    PostListView,
    PostListViewByTag,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views
from .feeds import LatestPostsFeed

urlpatterns = [
    # path('', views.home, name='blog-home'),
    path('', PostListView.as_view(), name='blog-home'),
    path('tag/<tag_slug>/', PostListViewByTag.as_view(), name='posts-list-by-tag'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('user-posts/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    # path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    # path('posts/<int:pk>/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('feed/', LatestPostsFeed(),name='posts-feed')
]
