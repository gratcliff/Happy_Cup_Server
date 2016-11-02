from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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