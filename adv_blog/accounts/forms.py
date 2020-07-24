from django import forms
from django.contrib.auth.models import User
from .models import UserModel
class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}), label='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}), label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}), label='')
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email')

    def clean_password(self):
        password1 = self.cleaned_data.get['password1']
        password2 = self.cleaned_data.get['password2']

        if  password1 and password2 and password1 != password2:
            raise forms.ValidationError('Enter same password for both')
        
        return password2

    def save(self, commit=True):
        user  = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit: 
            user.save()
        return user  
    
    
    
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}), label='')
    

class ProfileEditForm(forms.ModelForm):
   
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'profile_picture')

    # 
