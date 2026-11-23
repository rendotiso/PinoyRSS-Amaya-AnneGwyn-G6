from django.urls import path
from .views import dashboard_redirect

urlpatterns = [
    path('', dashboard_redirect, name='dashboard'),
]