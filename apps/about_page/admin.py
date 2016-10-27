from django.contrib import admin

from .forms import FullWidthSectionForm, StaffMemberEntryForm

from .models import FullWidthSection, StaffMemberEntry

from django.db import connection

# Register your models here.

# admin.site.disable_action('delete_selected')

class FullWidthSectionAdmin(admin.ModelAdmin):
	form = FullWidthSectionForm

class StaffMemberEntryAdmin(admin.ModelAdmin):
	form = StaffMemberEntryForm


admin.site.register(FullWidthSection, FullWidthSectionAdmin)
admin.site.register(StaffMemberEntry, StaffMemberEntryAdmin)