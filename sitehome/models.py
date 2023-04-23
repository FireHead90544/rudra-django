from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MySocialLink(models.Model):
    name = models.CharField(max_length=50)
    fa_classes = models.CharField(max_length=300)
    url = models.URLField(max_length=300)

    def __str__(self):
        return self.name.title()


class TimelineItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    date = models.DateField()

    def __str__(self):
        return f"{self.date.year} - {self.title}"
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField(max_length=2000)
    score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.timestamp.strftime('%d %b %Y, %H:%M')}"
    
class HireRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    budget = models.IntegerField()
    timeframe = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    message = models.TextField(max_length=2000)
    score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.budget}$] {self.name} - ({self.service}) [{self.timeframe}]"