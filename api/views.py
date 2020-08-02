import os

from dotenv import load_dotenv
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from posts.models import Group, Post

from .permissions import IsAdminOrReadOnly
from .serializers import GroupSerializer, PostSerializer
from .telegram import send_telegram

load_dotenv()
CHAT_ID = os.getenv("CHAT_ID")


class PostViewSet(ModelViewSet):
    queryset = Post.objects.filter(approved=True)
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()
        send_telegram(CHAT_ID)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
    serializer_class = GroupSerializer
