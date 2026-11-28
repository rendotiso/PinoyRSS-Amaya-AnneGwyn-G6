from django.core.management.base import BaseCommand

from feeds.categorizer import DEFAULT_CATEGORIES
from feeds.models import Category, NewsOutlet

OUTLETS = [
    ('Philippine Daily Inquirer', 'https://newsinfo.inquirer.net/feed'),
    ('Philstar', 'https://www.philstar.com/rss/headlines'),
    ('GMA News', 'https://data.gmanetwork.com/gno/rss/news/feed.xml'),
    ('Rappler', 'https://www.rappler.com/feed/'),
    ('Philippine News Agency', 'https://www.pna.gov.ph/latest.rss'),
    ('Manila Bulletin', 'https://mb.com.ph/rss/articles'),
]


class Command(BaseCommand):
    help = 'Creates the default categories and a starter library of Philippine news outlets.'

    def handle(self, *args, **kwargs):
        for name, desc in DEFAULT_CATEGORIES.items():
            Category.objects.get_or_create(category_name=name, defaults={'description': desc})
        for name, url in OUTLETS:
            _, created = NewsOutlet.objects.get_or_create(
                feed_url=url, defaults={'outlet_name': name, 'country': 'Philippines', 'is_active': True})
            self.stdout.write(('Added ' if created else 'Exists ') + name)
        self.stdout.write(self.style.SUCCESS('Library ready. Now run: python manage.py fetch_rss'))
