from django.forms import ModelForm
from .models import FullWidthSection, StaffMemberEntry



class FullWidthSectionForm(ModelForm):

	class Meta: 
		model = FullWidthSection
		fields = '__all__'

	def clean(self):
		cleaned_data = super(FullWidthSectionForm, self).clean()

		first_paragraph_length = len(cleaned_data.get("first_paragraph"))
		second_paragraph_length = len(cleaned_data.get("second_paragraph"))

		tot_length = first_paragraph_length + second_paragraph_length

		if second_paragraph_length == 0 and tot_length > 700:
			self.add_error('first_paragraph', 'Length of entry is too long for the provided space. Maximum 500 characters.')


		elif tot_length > 700:
			self.add_error('second_paragraph', 'Length of entry is too long for the provided space. Maximum 450 characters.')

class StaffMemberEntryForm(ModelForm):

	class Meta:
		model = StaffMemberEntry
		fields = '__all__'

	def clean(self):
		cleaned_data = super(StaffMemberEntryForm, self).clean()

		if len(cleaned_data.get("member_story")) > 300:
			self.add_error('member_story', "Length of member description is too long, max 300 characters.")

