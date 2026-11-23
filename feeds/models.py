from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.category_name

class NewsOutlet(models.Model):
    outlet_name = models.CharField(max_length=150)
    feed_url = models.URLField(unique=True)
    country = models.CharField(max_length=50, default='Philippines')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.outlet_name

class Article(models.Model):
    title = models.CharField(max_length=255)
    article_url = models.URLField(unique=True)
    summary = models.TextField(blank=True)
    published_at = models.DateTimeField()
    fetched_at = models.DateTimeField(auto_now_add=True)
    
    outlet = models.ForeignKey(NewsOutlet, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title