from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), # This now handles login/logout
    path('', include('dashboard.urls')),         # Redirect to dashboard
]