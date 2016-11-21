from django.contrib import admin

from .models import Carousel, Cafe_hours, Cafe_content
from .forms import Cafe_contentForm

from django.db import connection

# Register your models here.

# admin.site.disable_action('delete_selected')

class CarouselAdmin(admin.ModelAdmin):
	
	def has_add_permission (self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 6:
			return False
		else: 
			return True

class CafeContentAdmin(admin.ModelAdmin):
	form = Cafe_contentForm
	def has_add_permission (self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else: 
			return True

class CafeHoursAdmin(admin.ModelAdmin):
	def has_add_permission (self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else: 
			return True

admin.site.register(Carousel, CarouselAdmin)
admin.site.register(Cafe_hours, CafeHoursAdmin)
admin.site.register(Cafe_content, CafeContentAdmin)