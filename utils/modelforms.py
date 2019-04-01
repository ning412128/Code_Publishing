
from django import forms

class ModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ModelForm,self).__init__(*args,**kwargs)
        for name,fileds in self.fields.items():
            fileds.widget.attrs['class']='form-control'


