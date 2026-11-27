from django.contrib import admin
from .models import NewsOutlet, Category, Article


@admin.register(NewsOutlet)
class NewsOutletAdmin(admin.ModelAdmin):
    list_display = ('outlet_name', 'feed_url', 'country', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('outlet_name', 'feed_url')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'description')
    search_fields = ('category_name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'outlet', 'category', 'published_at')
    list_filter = ('outlet', 'category')
    search_fields = ('title', 'summary')
    date_hierarchy = 'published_at'
