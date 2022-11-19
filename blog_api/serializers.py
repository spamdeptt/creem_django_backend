from rest_framework import serializers
from blog.models import Posts

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id','category', 'title', 'author','excerpt','content','status']