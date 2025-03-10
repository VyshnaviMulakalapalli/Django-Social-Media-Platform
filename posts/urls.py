from django.urls import path
from .views import PostListCreateView, PostDetailView, LikePostView, CommentListView, FollowUserView, FollowerListView, NewsfeedView, FollowingListView

urlpatterns = [
    path("", PostListCreateView.as_view(), name="post-list-create"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:post_id>/like/", LikePostView.as_view(), name="like-post"),
    path("<int:post_id>/comments/", CommentListView.as_view(), name="comment-list-create"),
    path("follow/<int:user_id>/", FollowUserView.as_view(), name="follow-user"),
    path("<int:user_id>/followers/", FollowerListView.as_view(), name="follower-list"),
    path("<int:user_id>/following/", FollowingListView.as_view(), name="following-list"),
    path("newsfeed/", NewsfeedView.as_view(), name="newsfeed"),
]
