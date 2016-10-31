from django.forms import ModelForm
from .models import FullWidthSection, StaffMemberEntry



class FullWidthSectionForm(ModelForm):

	class Meta: 
		model = FullWidthSection
		fields = '__all__'

	def clean(self):
		cleaned_data = super(FullWidthSectionForm, self).clean()

		header_length = len(cleaned_data.get('header'))
		first_paragraph_length = len(cleaned_data.get("first_paragraph"))
		second_paragraph_length = len(cleaned_data.get("second_paragraph"))

		tot_length = first_paragraph_length + second_paragraph_length

		if header_length < 3:
			self.add_error('header', 'Please enter valid header text. 3 characters minumum.')

		if second_paragraph_length == 0 and tot_length > 700:
			self.add_error('first_paragraph', 'Length of entry is too long for the provided space. Maximum 700 characters. %s characters entered.' % (str(tot_length),))


		elif tot_length > 700:
			self.add_error('second_paragraph', 'Combined length of first and second paragraphs is too long for the provided space. Maximum 700 characters. %s characters entered.' % (str(tot_length),))
			self.add_error('first_paragraph', 'Combined length of first and second paragraphs is too long for the provided space. Maximum 700 characters. %s characters entered.' % (str(tot_length),))

class StaffMemberEntryForm(ModelForm):

	class Meta:
		model = StaffMemberEntry
		fields = '__all__'

	def clean(self):
		cleaned_data = super(StaffMemberEntryForm, self).clean()

		member_story_length = len(cleaned_data.get("member_story"))

		if member_story_length > 300:
			self.add_error('member_story', "Length of member description is too long. Maximum 300 characters. %s characters entered." % (str(member_story_length),))

