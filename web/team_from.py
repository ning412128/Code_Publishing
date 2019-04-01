from .models import Team
from utils.auth import ModelFormNew
from django.forms import ValidationError

class TeamForm(ModelFormNew):
    class Meta:
        model=Team
        fields='__all__'

    def clean_name(self):
        if self.instance.pk: return self.cleaned_data['name'].strip()
        name=self.cleaned_data['name']
        exist=Team.objects.filter(name=name).first()
        if exist:
            raise ValidationError('ip地址已经存在')
        else:
            return self.cleaned_data['name'].strip()
