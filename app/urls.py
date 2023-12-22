from django.urls import path
from app import views

urlpatterns = [
       path('post/<slug:slug>', views.post_page, name='post_page'),
       path('', views.index, name='home_page'),
       path('tag/<slug:slug>', views.tag_page, name='tag_page'),
       path('author/<slug:slug>', views.author_page, name='author_page'),
       path('search/', views.search_post, name='search'),
       path('about/', views.about, name='about'),
       path('accounts/register/', views.register_user, name='register'),
]

