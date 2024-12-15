import genericpath
from types import GenericAlias
from webbrowser import GenericBrowser
from django.forms import GenericIPAddressField
from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly  # type: ignore # A custom permission to ensure ownership control
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
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


class LikePostView(genericpath.GenericAPIView):
    """
    View for liking a post.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = GenericAlias.get_object_or_404(Post, pk=pk)  
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate a notification (ختياري)
        # Notification.objects.create(
        #     recipient=post.author,
        #     actor=request.user,
        #     verb="liked your post",
        #     target=post
        # )
        
        return Response({"detail": "Post liked successfully."}, status=status.HTTP_200_OK)


class UnlikePostView(GenericIPAddressField.GenericAPIView):
    """
    View for unliking a post.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = GenericBrowser.get_object_or_404(Post, pk=pk)  
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        like.delete()
        return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)
    
