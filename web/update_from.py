from .models import Issue
from utils.auth import ModelFormNew
from django.forms import ValidationError
from django import forms
class GitForm(ModelFormNew):
    class Meta:
        model=Issue
        fields=["team",'backup']



class FileForm(ModelFormNew):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),label="文件")
    class Meta:
        model=Issue
        fields=["team",'backup']