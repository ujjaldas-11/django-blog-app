from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tweet
from .serializers import TweetSerializer


class TweetViewset(viewsets.ModelViewSet):
    queryset = Tweet.objects.filter(published=True).order_by('-created_at')
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['craeted_at', 'title']

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            # Authors see their drafts too
            qs = Post.objects.filter(author=self.request.user) | qs
        return qs.distinct()

    def perform_create(self, serializers):
        serializers.save(author=self.request.user)


    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def publish(self, request, pk=None):
        tweet = self.get_object()
        if tweet.author != request.user:
            return Response({'detail': 'not yours'}, status=403)
        tweet.published = True
        tweet.save()
        return Response({"status": "published"})