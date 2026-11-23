from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import CustomUser

class SignupView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('accounts:login') 
    success_message = "Account created successfully! You can now log in."

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def form_invalid(self, form):
        form.add_error(None, "Invalid username or password.")
        return super().form_invalid(form)

class UserDashboardView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'dashboard/user_panel.html'
    success_url = reverse_lazy('accounts:user_panel') 

    def get_object(self):
        return self.request.user
    
    def test_func(self):
        return self.request.user.role == CustomUser.Roles.USER

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'dashboard/admin_panel.html'
    success_url = reverse_lazy('accounts:admin_panel') 

    def get_object(self):
        return self.request.user

    def test_func(self):
        return self.request.user.role == CustomUser.Roles.ADMIN