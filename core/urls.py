from django.urls import path
from .views import PostListCreateView, LikeCreateView, RegisterAPIView, UserProfileAPIView, CommentCreateAPIView, \
    NotificationListAPIView, CommentLikeCreateAPIView, home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),  # Home page (HTML)
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('likes/', LikeCreateView.as_view(), name='like-create'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('comments/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('notifications/', NotificationListAPIView.as_view(), name='notifications-list'),
    path('comments/like/', CommentLikeCreateAPIView.as_view(), name='comment-like-create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
