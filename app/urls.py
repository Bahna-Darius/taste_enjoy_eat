from django.urls import path
from app import views

urlpatterns = [
       path('post/<slug:slug>', views.post_page, name='post_page')
]

