from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.dateparse import parse_date

from bookmarks.models import Bookmark
from .models import Article, Category, NewsOutlet
from .text import fetch_article_html

PAGE_SIZE = 10


def attach_bookmarks(user, articles):
    """Sets article.bookmark_id (or None) on each article, then returns them as a list."""
    articles = list(articles)
    found = dict(Bookmark.objects.filter(user=user, article__in=articles).values_list('article_id', 'id'))
    for a in articles:
        a.bookmark_id = found.get(a.id)
    return articles


@login_required
def article_list(request):
    """Search, filter (outlet / category / date) and paginate the article library."""
    qs = Article.objects.select_related('outlet', 'category')

    q = request.GET.get('q', '').strip()
    outlet = request.GET.get('outlet', '')
    category = request.GET.get('category', '')
    date_from = parse_date(request.GET.get('date_from', '') or '')
    date_to = parse_date(request.GET.get('date_to', '') or '')

    if q:
        for term in q.split():
            qs = qs.filter(Q(title__icontains=term) | Q(summary__icontains=term))
    if outlet.isdigit():
        qs = qs.filter(outlet_id=int(outlet))
    if category.isdigit():
        qs = qs.filter(category_id=int(category))
    if date_from:
        qs = qs.filter(published_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(published_at__date__lte=date_to)

    page = Paginator(qs, PAGE_SIZE).get_page(request.GET.get('page'))

    params = request.GET.copy()
    params.pop('page', None)

    return render(request, 'feeds/article_list.html', {
        'page': page,
        'articles': attach_bookmarks(request.user, page.object_list),
        'outlets': NewsOutlet.objects.filter(is_active=True),
        'categories': Category.objects.all(),
        'q': q, 'outlet': outlet, 'category': category,
        'date_from': request.GET.get('date_from', '') if date_from else '',
        'date_to': request.GET.get('date_to', '') if date_to else '',
        'filters_active': any([q, outlet.isdigit(), category.isdigit(), date_from, date_to]),
        'querystring': params.urlencode(),
        'active_category': Category.objects.filter(pk=category).first() if category.isdigit() else None,
    })


@login_required
def article_detail(request, article_id):
    """In-app reading view: full text, with the source link at the bottom."""
    article = get_object_or_404(Article.objects.select_related('outlet', 'category'), pk=article_id)

    if not article.content and article.content_fetched_at is None:
        try:
            article.content = fetch_article_html(article.article_url)
        except Exception:
            article.content = ''
        article.content_fetched_at = timezone.now()   # don't hammer the source on every view
        article.save(update_fields=['content', 'content_fetched_at'])

    bookmark = Bookmark.objects.filter(user=request.user, article=article).first()
    return render(request, 'feeds/article_detail.html', {'article': article, 'bookmark': bookmark})


@login_required
def category_list(request):
    categories = Category.objects.annotate(
        article_count=Count('articles'),
        today_count=Count('articles', filter=Q(articles__published_at__gte=timezone.now() - timedelta(days=1))),
    )
    return render(request, 'feeds/category_list.html', {'categories': categories})
