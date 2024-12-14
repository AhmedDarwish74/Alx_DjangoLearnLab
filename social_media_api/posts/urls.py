from rest_framework.routers import DefaultRouter
from .views import UserFeedView
from .views import PostViewSet, CommentViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('feed/', UserFeedView.as_view(), name='user-feed'),
]
