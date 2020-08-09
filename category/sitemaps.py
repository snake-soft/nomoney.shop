from django.contrib.sitemaps import Sitemap
from .models import Category, CategoryStatus


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Category.objects.filter(status=CategoryStatus.PROVED)

    def lastmod(self, obj):
        return obj.modified
