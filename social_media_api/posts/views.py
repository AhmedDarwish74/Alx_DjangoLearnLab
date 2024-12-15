from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly  # A custom permission to ensure ownership control
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.generics import get_object_or_404
from .models import Post, Like
from rest_framework import status
from notifications.models import Notification


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Set the user as the author of the post
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """
        Optionally restricts the returned posts to the user's own posts.
        """
        queryset = Post.objects.all()
        user = self.request.user
        if user.is_authenticated:
            return queryset.filter(author=user)
        return queryset

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Set the user as the author of the comment
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """
        Optionally restricts the returned comments to the user's own comments or by post.
        """
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post_id', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        user = self.request.user
        if user.is_authenticated:
            return queryset.filter(author=user)
        return queryset
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

class LikePostView(APIView):
    """
    View for liking a post.
    This view allows a user to like a specific post. If the user has already liked the post,
    it returns an error message.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Fetch the post using its primary key
        post = get_object_or_404(Post, pk=pk)

        # Check if the user has already liked the post
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            # If the like already exists, return a message indicating so
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a notification for the post author indicating that the user liked their post
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )

        return Response({"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED)


class UnlikePostView(APIView):
    """
    View for unliking a post.
    This view allows a user to unlike a post they have previously liked. If the user hasn't liked the post,
    it returns an error message.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Fetch the post using its primary key
        post = get_object_or_404(Post, pk=pk)

        # Fetch the like instance if it exists
        like = Like.objects.filter(user=request.user, post=post).first()

        if not like:
            # If no like exists, return a message indicating the post hasn't been liked
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the like instance
        like.delete()

        # Create a notification for the post author indicating that the user unliked their post
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="unliked your post",
            target=post
        )

        return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)
