# from django.forms import ModelForm
# from .models import BlogPost



# class BlogPostForm(ModelForm):

# 	class Meta: 
# 		model = BlogPost
# 		fields = '__all__'

# 	def clean(self):
# 		cleaned_data = super(BlogPostForm, self).clean()

# 		link_title_length = len(cleaned_data.get("link_title"))


# 		if link_title_length > 300:
# 			self.add_error('link_title', 'Title length is too long, max 300 characters.')
