from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from bookmarks.models import Bookmark
from feeds.models import Article, Category, NewsOutlet
from feeds.views import attach_bookmarks


def _is_admin(user):
    return user.is_staff or user.role == 'admin'


@login_required
def dashboard_view(request):
    since = timezone.now() - timedelta(days=1)
    latest = attach_bookmarks(request.user, Article.objects.select_related('outlet', 'category')[:6])
    return render(request, 'dashboard/home.html', {
        'is_admin': _is_admin(request.user),
        'latest': latest,
        'bookmark_count': Bookmark.objects.filter(user=request.user).count(),
        'today_count': Article.objects.filter(published_at__gte=since).count(),
        'outlet_count': NewsOutlet.objects.filter(is_active=True).count(),
        'categories': Category.objects.annotate(n=Count('articles')).filter(n__gt=0).order_by('-n')[:8],
        'recent_bookmarks': Bookmark.objects.filter(user=request.user)
                                    .select_related('article', 'article__outlet')[:3],
    })


@login_required
def admin_panel_view(request):
    if not _is_admin(request.user):
        raise PermissionDenied
    return render(request, 'dashboard/admin_panel.html', {
        'outlets': NewsOutlet.objects.annotate(n=Count('articles')),
        'article_total': Article.objects.count(),
        'user_total': request.user.__class__.objects.count(),
        'category_total': Category.objects.count(),
    })
