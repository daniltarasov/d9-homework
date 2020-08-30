# from app.models import Post, Category, Author  
from app.models import Post, Category, Track, Album 
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response  
from django.contrib.auth.models import User
#чтобы не выводил ошибку о существующем пользователе:
# https://medium.com/django-rest-framework/dealing-with-unique-constraints-in-nested-serializers-dade33b831d9
from django.contrib.auth.validators import UnicodeUsernameValidator   



class AuthorForPostSerializer(serializers.ModelSerializer):
    # Post = PostSerializer(many=True, required=False)  
    username = serializers.CharField(help_text='Введите username существующего автора. Создать нового автора: "/author"')

    class Meta:  
        model = User  
        fields = ['username',]
        # fields = '__all__'
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
        }


class CatForPostSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, help_text="Можно не указывать, если такая категория уже существует. Обязательно для новой категории.")
    # slug = serializers.SlugField(read_only=True, help_text="Введите существующую категорию"))
    name = serializers.CharField(help_text="Введите название существующей категории или создайте новую.")
    class Meta:  
        model = Category
        fields = ['name', 'slug']
        # fields = '__all__'
        

class PostSerializer(serializers.ModelSerializer):
    # author = AuthorSerializer(required=False)
    author = AuthorForPostSerializer(required=True)
    category = CatForPostSerializer(required=False)

    class Meta:  
        model = Post  
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        # try:
        author_data = validated_data.pop('author', {})
        print(author_data)
        if author_data:
            try:
                # auth = Author.objects.get(username=author_data['username'])
                auth = User.objects.get(username=author_data['username'])
            except User.DoesNotExist:
                text = "Нет пользователя с именем {}".format(author_data['username'])
                raise ParseError(text)
            # except Author.DoesNotExist:
                # auth = User.objects.create(**author_data)
                # auth = Author.objects.create(**author_data)
            # except KeyError:
                # pass
        # else:

        
        category = validated_data.pop('category')
        print(category)

        name = category.get('name')
        slug = category.get('slug')
        if not name:
            text = "Не задана категория"
            raise ParseError(text)
        try:
            cat = Category.objects.get(name=name)
            if slug and slug != cat.slug:
                text = "Задан неверный Slug для существующей категории {}".format(name)
                raise ParseError(text)
        except Category.DoesNotExist:
            if not slug:
                text = "Задайте Slug для новой категории"
                raise ParseError(text)
            try:
                cat = Category.objects.get(slug=slug)
                text = "Category: Slug {} уже существует".format(slug)
                raise ParseError(text)
            except Category.DoesNotExist:
                pass
            cat = Category.objects.create(**category)

        if author_data:
            post = Post.objects.create(author=auth, category=cat, **validated_data)
        else:
            post = Post.objects.create(category=cat, **validated_data)       

        return post

# class PostforAuthorSerializer(serializers.ModelSerializer):
#     class Meta:  
#         model = Post  
#         fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    # posts = PostforAuthorSerializer(many=True, required=False)  #не отображаются посты
    class Meta:  
        model = User  
        fields = ['id', 'username', 'first_name', 'last_name']
        # fields = '__all__'
        # extra_kwargs = {
        #     'username': {
        #         'validators': [UnicodeUsernameValidator()],
        #     }
        # }


class PostForCategorySerializer(serializers.ModelSerializer):
    author = AuthorForPostSerializer(required=False)  

    class Meta:  
        model = Post  
        fields = ['title', "slug", 'content', 'author', "status", "publication_date", "updated"]


class CategorySerializer(serializers.ModelSerializer):

    posts = PostForCategorySerializer(many=True, required=False) 

    class Meta:  
        model = Category
        fields = ['id', 'slug', 'name', 'posts'] 

    def create(self, validated_data):
        name = validated_data.get('name')
        try:
            cat = Category.objects.get(name=name)
            text = "Уже есть категория с именем {}".format(name)
            raise ParseError(text)

        except Category.DoesNotExist:
            slug = validated_data.get('slug')
            if not slug:
                text = "Задайте Slug"
                raise ParseError(text)
            try:
                cat = Category.objects.get(slug=slug)
                text = "Category: Slug {} уже существует".format(slug)
                raise ParseError(text)
            except Category.DoesNotExist:
                pass

            cat = Category.objects.create(**validated_data)
        return cat


class CategoryDetailSerializer(serializers.ModelSerializer):
    posts = PostForCategorySerializer(many=True, required=False) 


    class Meta:  
        model = Category
        fields = ['id', 'slug', 'name', 'posts'] 
        # fields = ['id', 'slug', 'name', 'post_set'] 
        # fields = ['slug', 'name'] 
        # fields = '__all__'

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        if name != instance.name:
            try:
                cat = Category.objects.get(name=name)
                text = "Уже есть категория с именем {}".format(name)
                raise ParseError(text)
            except Category.DoesNotExist:
                pass
        slug = validated_data.get('slug')
        if not slug:
            text = "Задайте Slug"
            raise ParseError(text)
        try:
            cat = Category.objects.get(slug=slug)
            text = "Category: Slug {} уже существует".format(slug)
            raise ParseError(text)
        except Category.DoesNotExist:
            pass
        
        instance.name = validated_data.get('name', instance.name)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance









class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['order', 'title', 'duration']

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, required=False)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album