from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class PersonForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('Name', 'Linkedin_Email', 'password','profilephoto', 'Phone','Address','City','State','birth_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Profile'))

class scrapperprofileForm(forms.ModelForm):
    
    class Meta:
        model = scrapperprofile
        fields = ("profilelink",)
