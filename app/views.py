from rest_framework import generics  
from app.models import Post, Category, Album
from app.serializers import PostSerializer, CategorySerializer, CategoryDetailSerializer, AuthorSerializer, AlbumSerializer
from django.contrib.auth.models import User 

class PostList(generics.ListCreateAPIView):  
    queryset = Post.objects.all()  
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveDestroyAPIView):  
    queryset = Post.objects.all()  
    serializer_class = PostSerializer

class CategoryList(generics.ListCreateAPIView):  
    # queryset = Category.objects.all().annotate(posts=Post_set.all()) 
    # queryset = Category.objects.all().prefetch_related('toppings')
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):  
    queryset = Category.objects.all()  
    serializer_class = CategoryDetailSerializer

class AuthorList(generics.ListCreateAPIView):  
    queryset = User.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):  
    queryset = User.objects.all()  
    serializer_class = AuthorSerializer


    

class AlbumList(generics.ListCreateAPIView):  
    # queryset = Category.objects.all().annotate(posts=Post_set.all()) 
    # queryset = Category.objects.all().prefetch_related('toppings')
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer