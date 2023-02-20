
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User


class EmailCheckForm(forms.Form):
    # username = forms.CharField()
    username = forms.EmailField(label="Email Address *")
    #password1 = forms.CharField(widget=forms.PasswordInput, label="Password *")
    #password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password *")
    #first_name = forms.CharField(required=False, label='First Name')
    #last_name = forms.CharField(required=False, label='Last Name')

    # layout = Layout( 'username',
    #                 Row('password1', 'password2'),
    #                 Fieldset('Personal details',
    #                          Row('first_name', 'last_name'),))
    
    class Meta:
        model = User
        fields =  ('username',   )


class SignUpForm(UserCreationForm):
    #username = forms.CharField()
    #username = forms.EmailField(label="Email Address *")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password *")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password *")
    first_name = forms.CharField(required=False, label='First Name')
    last_name = forms.CharField(required=False, label='Last Name')

    # layout = Layout( 'username',
    #                 Row('password1', 'password2'),
    #                 Fieldset('Personal details',
    #                          Row('first_name', 'last_name'),))
    
    class Meta:
        model = User
        #readonly = ('username',)
        fields =  ('password1', 'password2','first_name', 'last_name',   )