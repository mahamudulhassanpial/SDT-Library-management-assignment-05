
from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView,UserLibraryAccountUpdateView, UserPasswordChangeView
from posts.views import return_book
 
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('change_password/', UserPasswordChangeView.as_view(),name="change_password"),
    path('profile/', UserLibraryAccountUpdateView.as_view(), name='profile' ),
    path('return_book/<int:order_id>/', return_book , name='return_book' ),
]