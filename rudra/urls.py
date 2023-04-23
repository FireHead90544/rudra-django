"""rudra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import BlogPostSitemap, PortfolioItemSitemap, StaticSitemap
from django.views.generic.base import TemplateView

sitemaps = {
    'static': StaticSitemap,
    'portfolio': PortfolioItemSitemap,
    'blog': BlogPostSitemap
}

urlpatterns = [
    path('', include('sitehome.urls')),
    path('blog/', include('blog.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^froala_editor/', include('froala_editor.urls')),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'sitehome.views.error_400'
handler403 = 'sitehome.views.error_403'
handler404 = 'sitehome.views.error_404'
handler500 = 'sitehome.views.error_500'