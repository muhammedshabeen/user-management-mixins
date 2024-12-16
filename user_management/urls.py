from django.urls import path
from .views import *

urlpatterns = [
    
    path('', UserLoginView.as_view(), name='user_login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', SignOutView.as_view(), name='signout'),
]