import feedparser
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from feeds.models import NewsOutlet, Article, Category

class Command(BaseCommand):
    help = 'Fetches RSS feeds from active News Outlets and saves them to the database'

    def handle(self, *args, **kwargs):
        outlets = NewsOutlet.objects.filter(is_active=True)
        
        if not outlets.exists():
            self.stdout.write(self.style.WARNING('No active news outlets found. Add some in the admin panel.'))
            return

        for outlet in outlets:
            self.stdout.write(f"Fetching feed for {outlet.outlet_name}...")
            
            feed = feedparser.parse(outlet.feed_url)
            
            if feed.bozo:
                self.stdout.write(self.style.ERROR(f"Failed to parse feed for {outlet.outlet_name}. Error: {feed.bozo_exception}"))
                continue

            default_category, _ = Category.objects.get_or_create(category_name="General")

            articles_added = 0

            for entry in feed.entries:
                published_date = timezone.now()
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_date = timezone.make_aware(timezone.datetime(*entry.published_parsed[:6]))
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published_date = timezone.make_aware(timezone.datetime(*entry.updated_parsed[:6]))

                summary = ""
                if hasattr(entry, 'summary'):
                    summary = entry.summary
                elif hasattr(entry, 'description'):
                    summary = entry.description

                article, created = Article.objects.get_or_create(
                    article_url=entry.link,
                    defaults={
                        'title': entry.title,
                        'summary': summary,
                        'published_at': published_date,
                        'outlet': outlet,
                        'category': default_category,
                    }
                )

                if created:
                    articles_added += 1

            self.stdout.write(self.style.SUCCESS(f"Successfully added {articles_added} new articles from {outlet.outlet_name}."))

        self.stdout.write(self.style.SUCCESS('Finished fetching all feeds.'))