from django.urls import path
from . import views
from .views import RegisterAPI  

urlpatterns = [
    # path('login/', views.login_view, name='login'),
    # path('signup/', views.signup_view, name='signup'),
    path('register/', RegisterAPI.as_view(), name='register'),
]
