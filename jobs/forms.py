from django import forms
from django.utils.translation import ugettext_lazy as _

class CreateJobForm(forms.Form):

	name = forms.CharField(label=_(u'Job name'),
                                 max_length=30,
                                 required=True)

	location = forms.CharField(label=_(u'Job location'),
								 max_length=30,
								 required=True)

	names_values = forms.CharField(widget=forms.Textarea,
								 label=_(u'Requirement'),
								 max_length=255,
								 required=False)

	intern_project = forms.BooleanField(label=_(u'Intern project?'), required=False)

	def save(self):
		name = self.cleaned_data['username']
		location = self.cleaned_data['location']

		new_job = super(CreateJobForm, self).save()
		return new_job