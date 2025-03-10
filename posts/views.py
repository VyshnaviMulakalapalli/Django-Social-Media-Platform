from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Like, Comment, Follow, Notification
from .serializers import PostSerializer, LikeSerializer, CommentSerializer, FollowSerializer, NotificationSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# Create and List Posts
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Retrieve, Update, and Delete a Post
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

# Like/Unlike a Post
class LikePostView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            like.delete()
            return Response({"message": "Unliked"}, status=200)
        
        Notification.objects.create(
            recipient=post.user,
            sender=request.user,
            type='like',
            post=post
        )
        return Response({"message": "Liked"}, status=201)

# List Comments on a Post
class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        comment = serializer.save(user=self.request.user, post=post)

        # Create notification for comment
        Notification.objects.create(
            recipient=post.user,
            sender=self.request.user,
            type='comment',
            post=post,
            comment=comment
        )

class FollowUserView(generics.GenericAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        following_user = get_object_or_404(User, id=user_id)
        if request.user == following_user:
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=following_user)
        
        if not created:
            follow.delete()
            return Response({"message": "Unfollowed"}, status=status.HTTP_200_OK)

        Notification.objects.create(
            recipient=following_user,
            sender=request.user,
            type='follow'
        )
        return Response({"message": "Followed"}, status=status.HTTP_201_CREATED)

class FollowerListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs["user_id"])
        return Follow.objects.filter(following=user)

class FollowingListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs["user_id"])
        return Follow.objects.filter(follower=user)  # This gets the users that the current user is following


class NewsfeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        followed_users = Follow.objects.filter(follower=self.request.user).values_list("following", flat=True)
        return Post.objects.filter(user__id__in=followed_users).order_by("-created_at")
    
class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

class MarkNotificationReadView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
        notification.read = True
        notification.save()
        return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)

