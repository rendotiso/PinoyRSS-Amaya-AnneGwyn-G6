from django.contrib import admin
from .models import NewsOutlet, Category, Article

@admin.register(NewsOutlet)
class NewsOutletAdmin(admin.ModelAdmin):
    list_display = ('outlet_name', 'feed_url', 'is_active')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'outlet', 'published_at')
    list_filter = ('outlet', 'category')

admin.site.register(Category)