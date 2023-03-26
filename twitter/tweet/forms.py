from django import forms
from .models import * 
class Tweetform(forms.ModelForm):
    body=forms.CharField(widget=forms.widgets.Textarea(
        attrs={'placeholder':'ENTER YOUR TWWET','class':'form-control'}
    ))
    class Meta:
        model=Tweet
        exclude=['user']