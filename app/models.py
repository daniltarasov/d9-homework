
from django.db import models  
from django.utils import timezone  
from django.contrib.auth.models import User 


class Post(models.Model):  
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE)  
    # author = models.ForeignKey('Author', null=True, blank=True, default=None, on_delete=models.CASCADE)  
    slug = models.SlugField(max_length=50, null=True, blank = True, unique=True)
    status = models.CharField(max_length=10, choices=[('D', 'draft'), ('P', 'published')])  
    content = models.TextField()
    updated = models.DateTimeField(default=timezone.now)  
    publication_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank = True, default=None, related_name="posts"
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title


class Category(models.Model):
    # slug = models.CharField(max_length=128)
    slug = models.SlugField(max_length=50, null=True, blank = True)  
    name = models.CharField(max_length=256)
    # todos_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} ({self.slug})'

# class Author(models.Model):
#     username = models.CharField(max_length=256)


class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)

class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE, null=True, blank = True)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        unique_together = ['album', 'order']
        ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.title)