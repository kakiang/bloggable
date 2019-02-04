from django.urls import path
from .views import (
    PostListView,
    PostListViewByTag,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    SearchPostView,
    CommentCreateView,
    post_like,
    PostLikeViewRedirect,
    PostLikeAPI,
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
    # path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/', CommentCreateView.as_view(), name='post-comment'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    # path('posts/<int:pk>/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('posts/search', SearchPostView.as_view(), name='post-search'),
    path('feed/', LatestPostsFeed(),name='posts-feed'),
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/like/', PostLikeViewRedirect.as_view(), name='post-clap' ),
    path('posts/<slug:slug>/api-like/', PostLikeAPI.as_view(), name='post-api-clap' ),
    # path('posts/<slug:slug>/api-like/', PostLikeAPI.as_view(), name='post-api-clap' ),
    # path('posts/<int:pk>/generate-pdf/', views.post_pdf,name='post-pdf' ),
    path('hello/', views.view_pdf,name='hello-pdf' )
]
