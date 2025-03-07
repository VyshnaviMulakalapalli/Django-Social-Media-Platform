from django.urls import path
from .views import PostListCreateView, PostDetailView, LikePostView, CommentListView

urlpatterns = [
    path("", PostListCreateView.as_view(), name="post-list-create"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:post_id>/like/", LikePostView.as_view(), name="like-post"),
    path("<int:post_id>/comments/", CommentListView.as_view(), name="comment-list-create"),
]
