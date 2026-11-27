from django.db import models
from django.db.models import Q


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)  # BR-06
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['category_name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name


class NewsOutlet(models.Model):
    outlet_name = models.CharField(max_length=150, unique=True)  # BR-07
    feed_url = models.URLField(unique=True)                      # BR-07
    country = models.CharField(max_length=50, default='Philippines')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['outlet_name']
        constraints = [
            # BR-05: only Philippine outlets may be registered
            models.CheckConstraint(
                condition=Q(country='Philippines'),
                name='outlet_country_is_philippines',
            ),
        ]

    def __str__(self):
        return self.outlet_name


class Article(models.Model):
    title = models.CharField(max_length=255)
    article_url = models.URLField(max_length=500, unique=True)
    summary = models.TextField(blank=True)
    published_at = models.DateTimeField()
    fetched_at = models.DateTimeField(auto_now_add=True)

    # In-app viewing: sanitised full text (filled from the feed or lazily from the source page)
    content = models.TextField(blank=True)
    content_fetched_at = models.DateTimeField(null=True, blank=True)

    outlet = models.ForeignKey(NewsOutlet, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='articles')

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
