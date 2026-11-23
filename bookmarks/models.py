from django.db import models
from django.conf import settings
from feeds.models import Article

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bookmarked_by')
    bookmarked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent a user from bookmarking the same article twice
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"