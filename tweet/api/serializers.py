from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Tweet

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True,
        required=False,
        default=serializers.CurrentUserDefault()
    )        

    class Meta:
        model = Tweet
        fields = ['id', 'title', 'content', 'photo', 'user', 'user_id', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'author']

    def validate(self, data):
        if not data.get('title'):
            raise serializers.ValidationError({'title': 'Title field is required'})
        if not data.get('content'):
            raise serializers.ValidationError(({'content': 'Content field required'}))
        return data
