from .models import UserProfile
from utils.auth import ModelFormNew
from django.forms import ValidationError
class UserForm(ModelFormNew):
    class Meta:
        model=UserProfile
        fields='__all__'

    def clean_email(self):
        if self.instance.pk: return self.cleaned_data['email'].strip()
        email=self.cleaned_data['email']
        exist=UserProfile.objects.filter(email=email).first()
        if exist:
            raise ValidationError('邮箱已经存在')
        else:
            return self.cleaned_data['email'].strip()
