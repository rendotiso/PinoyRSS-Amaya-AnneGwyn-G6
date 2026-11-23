from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from feeds.models import Article
from .models import Bookmark

@login_required
def article_list(request):
    """Read: Shows all available RSS articles."""
    articles = Article.objects.all().order_by('-published_at')
    return render(request, 'feeds/article_list.html', {'articles': articles})

@login_required
def add_bookmark(request, article_id):
    """Create: Add an article to the logged-in user's bookmarks."""
    article = get_object_or_404(Article, id=article_id)
    
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, article=article)
    
    if created:
        messages.success(request, "Article bookmarked successfully!")
    else:
        messages.info(request, "You already bookmarked this article.")
        
    return redirect('article_list')

@login_required
def my_bookmarks(request):
    """Read: Shows ONLY the logged-in user's bookmarks."""

    bookmarks = Bookmark.objects.filter(user=request.user).order_by('-bookmarked_at')
    return render(request, 'bookmarks/my_bookmarks.html', {'bookmarks': bookmarks})

@login_required
def delete_bookmark(request, bookmark_id):
    """Delete: Remove a bookmark. Role-based security check included."""
    bookmark = get_object_or_404(Bookmark, id=bookmark_id)
    
    if request.user == bookmark.user or request.user.role == 'admin':
        bookmark.delete()
        messages.success(request, "Bookmark removed.")
    else:
        messages.error(request, "You do not have permission to delete this.")
        
    return redirect('my_bookmarks')