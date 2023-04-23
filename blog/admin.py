from django.contrib import admin
from .models import *

admin.site.site_header = "Rudransh Joshi"
admin.site.site_title = "Rudrash Joshi | Dashboard"
admin.site.index_title = "Welcome to Admin Panel"

# Register your models here.
# class BlogPostAdmin(admin.ModelAdmin):
#     class Media:
#         js = ('blog/js/prism.js',)
#         css = {
#             'all': ('blog/css/prism-atom-dark.css',)
#         }

# admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register((PostAuthor, BlogPost, BlogComment, PostView, PostLike, ))