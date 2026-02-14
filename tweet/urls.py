from django.urls import path
from . import views

urlpatterns = [
    path('', views.tweet_list, name="tweet_list"),
    path('create/', views.create_tweet, name="create_tweet"),
    path('edit/<int:tweet_id>/', views.update_tweet, name="edit-tweet"),
    path('delete/<int:tweet_id>/', views.delete_tweet, name="delete-tweet"),
]