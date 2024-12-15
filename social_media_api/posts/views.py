from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly  # A custom permission to ensure ownership control
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


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({"detail": "You have already liked this post."}, status=400)
        
        # Create the like
        Like.objects.create(user=request.user, post=post)
        
        # Generate a notification
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )
        return Response({"detail": "Post liked successfully."}, status=201)


class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"detail": "You have not liked this post."}, status=400)
        
        like.delete()
        return Response({"detail": "Post unliked successfully."}, status=200)
    
class LikePostView(APIView):
    """
    View for liking a post.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Use generics.get_object_or_404 to fetch the post
        post = get_object_or_404(Post, pk=pk)

        # Use Like.objects.get_or_create to like the post
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a notification for the post author
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
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Use generics.get_object_or_404 to fetch the post
        post = get_object_or_404(Post, pk=pk)

        # Fetch the like instance if it exists
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the like instance
        like.delete()

        return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)