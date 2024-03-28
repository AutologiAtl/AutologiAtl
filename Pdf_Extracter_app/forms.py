# fileupload/forms.py
from django import forms
from .models import UploadedFile
# from multiupload.fields import MultiFileField

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file1', 'file2']

    file1 = forms.FileField(label='Invoice/Measho')
    file2 = forms.FileField(label='Booking Confirmation')
    # files = forms.FileField(label='Booking Confirmation')
    # files = forms.FileField(label='Excel File', widget=forms.ClearableFileInput(attrs={'multiple': True}))

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
