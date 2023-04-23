from django.db import models

# Create your models here.

class PortfolioItem(models.Model):
    def get_upload_path(instance, filename):
        return f'portfolio/{instance.slug}/images/{filename}'

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    date = models.DateField()
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to=get_upload_path)
    author = models.CharField(max_length=100, blank=True, null=True)
    project_link = models.URLField(max_length=500, blank=True, null=True)
    tags = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.title

class PortfolioImage(models.Model):
    def get_upload_path(instance, filename):
        return f'portfolio/{instance.portfolio_item.slug}/images/{filename}'

    portfolio_item = models.ForeignKey(PortfolioItem, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path)
    alt = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.portfolio_item.title} - [{self.id}]"