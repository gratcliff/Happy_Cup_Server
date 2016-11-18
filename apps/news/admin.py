from django.contrib import admin
from .models import BlogPost
from django.db import connection
from tinymce.widgets import TinyMCE



# Register your models here.
class BlogPostAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'image_url')
	

admin.site.register(BlogPost, BlogPostAdmin)