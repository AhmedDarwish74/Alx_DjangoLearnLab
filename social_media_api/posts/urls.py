from rest_framework.routers import DefaultRouter
from .views import UserFeedView
from .views import PostViewSet, CommentViewSet
from django.urls import path
from .views import LikePostView, UnlikePostView


urlpatterns = [
    path('feed/', UserFeedView.as_view(), name='user_feed'),
     path('<int:pk>/like/', LikePostView.as_view(), name='like_post'),
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike_post'),
]

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
urlpatterns = router.urls


