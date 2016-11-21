from django.forms import ModelForm
from .models import Cafe_content



class Cafe_contentForm(ModelForm):

	class Meta: 
		model = Cafe_content
		fields = '__all__'

	def clean(self):
		cleaned_data = super(Cafe_contentForm, self).clean()

		text_length = len(cleaned_data.get('description'))

		
		if text_length > 600:
			self.add_error('description', 'Length of entry is too long for the provided space. Maximum 600 characters. %s characters entered.' % (str(tot_length),))


		elif text_length < 50:
			self.add_error('description', 'Entry is too short, %s characters entered. Minimum 50 characters.' % (str(tot_length),))
			

