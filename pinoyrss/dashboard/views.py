from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser 

@login_required
def dashboard_redirect(request):
    if request.user.role == CustomUser.Roles.ADMIN:
        return redirect('accounts:admin_panel') 
    return redirect('accounts:user_panel')     