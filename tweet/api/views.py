from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Tweet
from .serializers import TweetSerializer


class TweetViewSet(viewsets.ModelViewSet):
    # queryset = Tweet.objects.filter(published=True).order_by('-created_at')
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['user']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']

    def get_queryset(self):
        return Tweet.objects.all().order_by('-created_at')


    def perform_create(self, serializers):
        serializers.save(user=self.request.user)


    