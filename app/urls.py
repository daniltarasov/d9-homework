from app.views import PostList, PostDetail, CategoryList, CategoryDetail, AuthorList, AuthorDetail, AlbumList
from django.urls import path  

app_name = 'app'  
urlpatterns = [  
    path('', PostList.as_view(), name='post-list'),  
    path('<int:pk>', PostDetail.as_view(), name='post-detail'),
    path('category', CategoryList.as_view(), name='cat-list'),
    path('category/<int:pk>', CategoryDetail.as_view(), name='cat-detail'),
    path('author', AuthorList.as_view(), name='auth-list'),
    path('author/<int:pk>', AuthorDetail.as_view(), name='auth-detail'),
    path('album', AlbumList.as_view(), name='al-list'),    
]