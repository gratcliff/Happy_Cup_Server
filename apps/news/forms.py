from django import forms
from .models import BlogPost

from tinymce.widgets import TinyMCE



class BlogPostForm(forms.ModelForm):

	text = forms.CharField(widget=TinyMCE(attrs={'cols':80, 'rows':30}))

	class Meta: 
		model = BlogPost
		fields = '__all__'