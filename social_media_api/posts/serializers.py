from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'content', 'created_at', 'updated_at')

    def validate_content(self, value):
        # Add any custom validation logic if needed
        if not value:
            raise serializers.ValidationError("Content cannot be empty.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'content', 'created_at', 'updated_at')

    def validate_content(self, value):
        # Ensure that comment content isn't empty
        if not value:
            raise serializers.ValidationError("Comment content cannot be empty.")
        return value
