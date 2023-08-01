from django.urls import path
from . import views

urlpatterns = [
    path('', views.query_chatbot, name='query_chatbot'),
    path('post/new/', views.post_new, name='post_new'),
]