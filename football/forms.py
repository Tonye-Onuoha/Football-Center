from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Comments,Profiles
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({'id':'username','class':'form-control','placeholder':'Enter a username'})
        self.fields['password1'].widget.attrs.update({'id':'password1','class':'form-control','placeholder':'Enter a password'})
        self.fields['password2'].widget.attrs.update({'id':'password2','class':'form-control','placeholder':'Confirm your password'})

    first_name = forms.CharField(widget=forms.TextInput(attrs={'id':'firstname','class':'form-control','placeholder':'Enter your first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id':'lastname','class':'form-control','placeholder':'Enter your last name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id':'email','class':'form-control','placeholder':'markjohnson@gmail.com'}))

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

        
class PostForm(forms.Form):
    post = forms.CharField(label="",widget=forms.Textarea())

        
class PostModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['post'].widget.attrs.update({'class':'post-model-form','placeholder':'Enter a post'})
    class Meta:
        model = Comments
        fields = ['post']
        labels = {'post':''}
        help_texts = {'post':''}


class ReplyPostForm(forms.Form):
    reply = forms.CharField(label='',help_text='Enter a reply',max_length=150,widget=forms.Textarea())

    
class QuoteForm(forms.Form):
    quote = forms.CharField(label='',help_text='Enter a quote',max_length=150,widget=forms.Textarea())


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['bio','image']
        help_texts = {'bio':_('Tell us about yourself'),}
        widgets = {'bio': forms.Textarea(attrs={'placeholder':'Tell us about yourself here.'})}
