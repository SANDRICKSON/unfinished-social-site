from django.shortcuts import render
from rest_framework import generics, permissions, viewsets

from .forms import RegisterForm
from .models import Post, Like, Comment, CommentLike
from .serializers import PostSerializer, LikeSerializer, CommentSerializer, CommentLikeSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer

from rest_framework import permissions, status, generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import permissions, generics
from rest_framework.response import Response
from .serializers import NotificationSerializer
from .models import Notification

class NotificationListAPIView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # მხოლოდ მომხმარებლის შეტყობინებების დაბრუნება
        return self.queryset.filter(user=self.request.user)

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user  # მხოლოდ ავტორიზებულ იუზერს შეუძლია თავისი პროფილის ნახვა ან რედაქტირება

    def update(self, request, *args, **kwargs):
        # აქ შეგიძლიათ დაამატოთ მომხმარებლის შეცვლის ლოგიკა (მაგ. პაროლის შეცვლა)
        return super().update(request, *args, **kwargs)

# რეგისტრაცია
class RegisterAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        user = get_user_model().objects.get(username=request.data["username"])
        refresh = RefreshToken.for_user(user)
        response.data['access'] = str(refresh.access_token)
        response.data['refresh'] = str(refresh)

        return response


# Feed - ყველა პოსტი
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Like შექმნა
class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # პოსტზე კომენტარის გაკეთება
        post_id = self.request.data.get('post')
        post = Post.objects.get(id=post_id)
        serializer.save(user=self.request.user, post=post)
class CommentLikeCreateAPIView(generics.CreateAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # კომენტარის ლაიქის შექმნა
        comment_id = self.request.data.get('comment')
        comment = Comment.objects.get(id=comment_id)
        serializer.save(user=self.request.user, comment=comment)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

def home(request):
    return render(request, 'home.html')