from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    is_admin = request.user.is_staff or request.user.role == 'admin'
    
    context = {
        'is_admin': is_admin,
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def admin_panel_view(request):
    if not request.user.is_staff and request.user.role != 'admin':
        raise PermissionDenied
        
    return render(request, 'dashboard/admin_panel.html')