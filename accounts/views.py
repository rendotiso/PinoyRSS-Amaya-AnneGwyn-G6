from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from bookmarks.models import Bookmark
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import CustomUser


class SignupView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('accounts:login')
    success_message = 'Account created. You can now log in.'


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        form.add_error(None, 'Invalid username or password.')
        return super().form_invalid(form)


class LoggedOutView(TemplateView):
    """Confirmation screen shown after logging out."""
    template_name = 'registration/logged_out.html'


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """View and update account details (all roles)."""
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = 'Profile updated.'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        mine = Bookmark.objects.filter(user=self.request.user)
        ctx['bookmark_count'] = mine.count()
        ctx['recent_bookmarks'] = mine.select_related('article', 'article__outlet')[:3]
        return ctx
