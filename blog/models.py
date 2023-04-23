from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from django.utils.timezone import now

# Create your models here.

class PostAuthor(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    about = models.TextField()
    avatar = models.ImageField(upload_to="blog/authors/")
    github = models.URLField(max_length=300, default="https://github.com/")
    instagram = models.URLField(max_length=300, default="https://instagram.com/")
    twitter = models.URLField(max_length=300, default="https://twitter.com/")
    email = models.EmailField(max_length=300, default="thisemail@doesnotexists.com")

    def __str__(self):
        return self.name
    
class BlogPost(models.Model):
    def get_upload_path(instance, filename):
        return f'blog/{instance.slug}/images/{filename}'

    title = models.CharField(max_length=200)
    tldr = models.CharField(max_length=500)
    content = FroalaField()
    slug = models.SlugField(unique=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=100, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=get_upload_path)
    author = models.ForeignKey(PostAuthor, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.tags = ", ".join([tag.strip().title() for tag in self.tags.split(",")])
        super().save(*args, **kwargs)

    @property
    def views(self):
        return PostView.objects.filter(post=self).count()
    
    @property
    def likes(self):
        return PostLike.objects.filter(post=self).count()
    
    def __str__(self):
        return self.title

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.comment [:20]}... by {self.user.username}"
    
class PostView(models.Model):
    ip = models.GenericIPAddressField()
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ip} viewed {self.post.title}"
    
class PostLike(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} liked {self.post}"