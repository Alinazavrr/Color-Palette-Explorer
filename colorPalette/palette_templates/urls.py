from django.contrib import admin
from django.urls import path
from .views import HomePageView

# urls.py

urlpatterns = [
    path('', HomePageView.as_view(), name='main_page'),
]
                                                                                               