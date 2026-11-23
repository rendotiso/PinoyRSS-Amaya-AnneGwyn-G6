from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('bookmark/add/<int:article_id>/', views.add_bookmark, name='add_bookmark'),
    path('bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    path('bookmark/delete/<int:bookmark_id>/', views.delete_bookmark, name='delete_bookmark'),
]