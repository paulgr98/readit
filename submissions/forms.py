from django import forms
from subreadits.models import Subreadit

class SubmissionForm(forms.Form):
    subreadit = forms.ModelChoiceField(queryset=Subreadit.objects.all())
    title = forms.CharField(label='Title', max_length=255)
    image_url = forms.CharField(label='Image Url (optional)', max_length=5000, required=False)
    text = forms.CharField(label='Text (optional)', max_length=5000, widget=forms.Textarea, required=False)