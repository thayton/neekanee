from django import forms
from models import *

class RegistrationForm(forms.Form):
    username = forms.CharField(label=u'Username', max_length=30)
    email = forms.EmailField(label=u'Email')
    password1 = forms.CharField(
        label=u'Password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label=u'Password (Again)',
        widget=forms.PasswordInput()
    )

class UploadJobsForm(forms.Form):
    """ 
    Upload JSON-encoded file of company jobs 
    """
    file = forms.FileField()
    
class JobAlertForm(forms.ModelForm):
    class Meta:
        model = JobAlert
        exclude = ('user','key')

class JobBookmarkForm(forms.ModelForm):
    class Meta:
        model = JobBookmark
        exclude = ('user',)
