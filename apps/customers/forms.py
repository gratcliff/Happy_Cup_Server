from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Customer
from ..locations.mapsapi import validate_address




class UserRegisterForm(UserCreationForm):


	class Meta:

		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def clean(self):
		cleaned_data = super(UserRegisterForm, self).clean()
		duplicate = User.objects.filter(email__iexact=cleaned_data['email'])
		if duplicate:
			self.add_error('email', 'A user with that email address already exists.')

	def save(self, commit=True):
		user = super(UserRegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
			return user

class UserEditForm(forms.ModelForm):

	class Meta:

		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def clean(self):
		cleaned_data = super(UserEditForm, self).clean()
		if self.errors:
			return


class CustomerShippingForm(forms.ModelForm):

	class Meta:

		model = Customer
		fields = "__all__"

	def clean(self):
		cleaned_data = super(CustomerShippingForm, self).clean()
		if self.errors:
			return

		final_address = "%s %s, %s %s, %s" % (cleaned_data["address"], cleaned_data["address2"], cleaned_data["city"], cleaned_data["state"], cleaned_data["zipcode"])

		(address, components) = validate_address(final_address)

		if 'error' in address:
			if address['error'] == 'no result':
				self.add_error('address', address['message'])
			else:
				cleaned_data['api_error'] = address['message']
		else:	
			cleaned_data['verify_address'] = components


