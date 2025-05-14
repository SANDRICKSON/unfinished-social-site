from rest_framework import serializers
from .models import User, Post, Like, Comment, Notification, CommentLike, Reply


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'avatar']


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'caption', 'image', 'video', 'created_at', 'likes_count']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'content', 'is_read', 'created_at']


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['user', 'comment', 'created_at']


class ReplySerializer(serializers.ModelSerializer):
    user = UserSerializer()  # ვაჩვენოთ მომხმარებელი პასუხში
    comment = CommentSerializer()  # ვაჩვენოთ კომენტარი, რომელზეც პასუხი არის

    class Meta:
        model = Reply
        fields = ['id', 'user', 'comment', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']


# ისევ ერთიანი `Post` სერიალიზატორი:
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'caption', 'image', 'video', 'created_at', 'likes_count']


# ისევ ერთიანი `Like` სერიალიზატორი:
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']


# ისევ ერთიანი `Comment` სერიალიზატორი:
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']
