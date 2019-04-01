from .models import Cron
from utils.auth import ModelFormNew
from django.forms import ValidationError

class CronForm(ModelFormNew):
    class Meta:
        model=Cron
        exclude=['create_user','time']

    def clean_name(self):
        if self.instance.pk: return self.cleaned_data['name'].strip()
        name=self.cleaned_data['name']
        exist=Cron.objects.filter(name=name).first()
        if exist:
            raise ValidationError('ip地址已经存在')
        else:
            return self.cleaned_data['name'].strip()
