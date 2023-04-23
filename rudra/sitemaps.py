from django.contrib.sitemaps import Sitemap
from blog.models import BlogPost
from portfolio.models import PortfolioItem
from django.urls import reverse

class BlogPostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.9

    def items(self):
        return BlogPost.objects.all()
    
    def lastmod(self, obj):
        return obj.publish_date
    
    def location(self, obj):
        return f"/blog/{obj.slug}/"
    
class PortfolioItemSitemap(Sitemap):
    changefreq = "never"
    priority = 0.9

    def items(self):
        return PortfolioItem.objects.all()
    
    def lastmod(self, obj):
        return obj.date
    
    def location(self, obj):
        return f"/portfolio/{obj.slug}/"
    
class StaticSitemap(Sitemap):
    changefreq = "never"
    priority = 1.0

    def items(self):
        return [
            "allmylinks", "timeline", "hireme",
            "PortfolioHome",
            "BlogHome", "BlogLogin", "BlogRegister", "UserDashboard", "BlogSearch"
        ]
    
    def location(self, obj):
        return reverse(obj)