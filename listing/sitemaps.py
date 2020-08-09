from django.contrib.sitemaps import Sitemap
from .models import Push, Pull, ListingStatus


class ListingSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    type = None

    def items(self):
        return self.type.objects.filter(status=ListingStatus.CREATED)

    def lastmod(self, obj):
        return obj.modified


class PushSitemap(ListingSitemap):
    type = Push


class PullSitemap(ListingSitemap):
    type = Pull
