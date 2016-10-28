from django.contrib import admin


from .models import BlogPost

from django.db import connection

# Register your models here.
class BlogPostAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'link_title')

admin.site.register(BlogPost, BlogPostAdmin)