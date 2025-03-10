from rest_framework import serializers
from .models import Post, Like, Comment, Follow, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "user", "caption", "image", "video", "created_at", "likes_count", "comments_count"]
        read_only_fields = ["user"]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]
        read_only_fields = ["user"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "post", "text", "created_at"]
        read_only_fields = ["user"]

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]
        read_only_fields = ["follower"]
        
class NotificationSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username')
    post_caption = serializers.CharField(source='post.caption', allow_null=True)
    comment_text = serializers.CharField(source='comment.text', allow_null=True)

    class Meta:
        model = Notification
        fields = ['id', 'sender_username', 'type', 'post_caption', 'comment_text', 'created_at', 'read']

