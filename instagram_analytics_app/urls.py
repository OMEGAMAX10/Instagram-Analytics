from django.urls import path
from instagram_analytics_app import views

urlpatterns = [
    path('', views.InstagramAnalyticsIndexView.as_view(), name='index'),
    path('followers-analytics/', views.FollowersAnalyticsView.as_view(), name='followers-analytics'),
]
