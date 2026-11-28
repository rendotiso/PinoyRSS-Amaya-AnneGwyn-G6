from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import RedirectView

from .views import CustomLoginView, LoggedOutView, ProfileView, SignupView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logged-out/', LoggedOutView.as_view(), name='logged_out'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/', RedirectView.as_view(pattern_name='accounts:profile'), name='user_panel'),
    path('admin-panel/', RedirectView.as_view(pattern_name='accounts:profile'), name='admin_panel'),
]
