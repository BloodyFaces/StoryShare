from django import forms


from .models import Story, ProfileInfo, Comment

class StoryForm(forms.ModelForm):
	class Meta:
		model = Story
		fields = [
			'topic',
			'content',
		]


class ProfileForm(forms.ModelForm):

	name = forms.CharField(max_length=30, required=True)
	surname = forms.CharField(max_length=150, required=True)

	class Meta:
		model = ProfileInfo
		fields = [
			'name',
			'surname',
			'image',
		]


class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ['content', ]