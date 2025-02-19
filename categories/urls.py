from django.contrib import admin
from django.urls import path, include
from . import views
from core.views import  home

urlpatterns = [
    path('add/', views.add_catagory, name='add_catagory'),
    path('category/<slug:category_slug>/', home, name='category_wise_post'),
]
