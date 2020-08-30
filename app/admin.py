from django.contrib import admin
from app.models import Post, Category, Album, Track
from django.contrib.auth.models import User 

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass