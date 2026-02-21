from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Tweet

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source=author,
        write_only=True,
        default=serializers.CurrentUserDefault()
    )        

    class Meta:
        model = Tweet
        fields = ['id', 'title', 'content', 'photo', 'author', 'author_id', 'created_at', 'updated_at', 'published', 'is_draft']
        read_only_fields = ['created_at', 'updated_at', 'author']

    def validate(self, data):
        if not data.get('title'):
            raise serializers.ValidationError({'title': 'title field required'})
        return data
