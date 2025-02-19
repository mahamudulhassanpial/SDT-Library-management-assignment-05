from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('add/', views.add_Post, name='add_Post'),
    path('add/', views.AddPostCreateView.as_view(), name='add_Post'),
    # path('edit/<int:id>', views.edit_Post, name='edit_Post'),
    path('edit/<int:id>/', views.EditPostView.as_view(), name='edit_Post'),
    # path('delete/<int:id>', views.delete_Post, name='delete_Post'),
    path('delete/<int:id>/', views.DeletePostView.as_view(), name='delete_Post'),
    # path('details/<int:pk>/', views.DetailPostView.as_view(), name='detail_Post'),
    path('details/<int:pk>/', views.PostDetailView.as_view(), name='detail_Post'),
]