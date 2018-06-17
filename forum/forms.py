from django.forms import ModelForm, Textarea, TextInput
from .models import Thread, Response

# CSS class to add to every form widget to make bootstrap nice
BOOSTRAP_FORM_WIDGET_attrs = {
	'class': 'form-control'
}

BOOSTRAP_FORM_WIDGET_attrs_md = {
	'class': 'form-control markdown-input'
}

class ThreadForm(ModelForm):
	class Meta:
		model = Thread
		fields = ['title', 'body']
		widgets = {
			'title': TextInput(attrs=BOOSTRAP_FORM_WIDGET_attrs),
			'body': Textarea(attrs=BOOSTRAP_FORM_WIDGET_attrs_md),
		}

# Like the thread edit form but also has a field for location
# to allow users to move their threads
class ThreadEditForm(ModelForm):
	class Meta:
		model = Thread
		fields = ['title', 'body', 'forum']
		widgets = {
			'title': TextInput(attrs=BOOSTRAP_FORM_WIDGET_attrs),
			'body': Textarea(attrs=BOOSTRAP_FORM_WIDGET_attrs_md),
		}

# form that goes under a post for users to reply to
# presented as a "comment" style thing
class ResponseForm(ModelForm):
	class Meta:
		model = Response
		fields = ['body']
		widgets = {
			'body': Textarea(attrs=BOOSTRAP_FORM_WIDGET_attrs_md),
		}

		labels = {
			'body': '',
		}
