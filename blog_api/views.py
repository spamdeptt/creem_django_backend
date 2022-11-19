from rest_framework import generics
from blog.models import Posts
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Posts.postobjects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer