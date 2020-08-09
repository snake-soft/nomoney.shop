from django.urls.base import reverse
from django.contrib import sitemaps
from listing.sitemaps import PushSitemap, PullSitemap
from category.sitemaps import CategorySitemap


class HighPrioSitemap(sitemaps.Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return ['home', 'about', 'donate']

    def location(self, item):
        return reverse(item)


class LowPrioSitemap(sitemaps.Sitemap):
    priority = 0.3
    changefreq = 'weekly'

    def items(self):
        return ['terms', 'impressum']

    def location(self, item):
        return reverse(item)


SITEMAPS = {
    'high_prio': HighPrioSitemap,
    'categories': CategorySitemap,
    'pushs': PushSitemap,
    'pulls': PullSitemap,
    'low_prio': LowPrioSitemap,
    }
