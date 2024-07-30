from django.urls import path
from .views import NewsListAPIViews


urlpatterns = [
    path('', NewsListAPIViews.as_view(), name='news-list'),

]