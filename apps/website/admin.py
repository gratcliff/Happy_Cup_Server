from django.contrib import admin

from .models import CafeCarouselImage, Cafe_hours, Cafe_content, ContactPage
from .forms import Cafe_contentForm


# Register your models here.

admin.site.disable_action('delete_selected')


class CafeCarouselImageAdmin(admin.ModelAdmin):
	
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

	def has_delete_permission(self, request, obj=None):
		return False

class CafeHoursAdmin(admin.ModelAdmin):
	def has_add_permission (self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else: 
			return True
	def has_delete_permission(self, request, obj=None):
		return False

class ContactPageAdmin(admin.ModelAdmin):
	def has_add_permission (self, request):
		num_objects = self.model.objects.count()
		if num_objects >= 1:
			return False
		else: 
			return True
	def has_delete_permission(self, request, obj=None):
		return False


admin.site.register(CafeCarouselImage, CafeCarouselImageAdmin)
admin.site.register(Cafe_hours, CafeHoursAdmin)
admin.site.register(Cafe_content, CafeContentAdmin)
admin.site.register(ContactPage, ContactPageAdmin)






