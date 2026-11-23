from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import SignupView, CustomLoginView, UserDashboardView, AdminDashboardView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('dashboard/', UserDashboardView.as_view(), name='user_panel'),
    path('admin-panel/', AdminDashboardView.as_view(), name='admin_panel'),
]