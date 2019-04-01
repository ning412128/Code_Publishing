from .models import Host
from utils.auth import ModelFormNew
from django.forms import ValidationError

class HostForm(ModelFormNew):
    class Meta:
        model=Host
        fields='__all__'

    def clean_hostip(self):
        if self.instance.pk: return self.cleaned_data['hostip'].strip()
        hostip=self.cleaned_data['hostip']
        exist=Host.objects.filter(hostip=hostip).first()
        if exist:
            raise ValidationError('ip地址已经存在')
        else:
            return self.cleaned_data['hostip'].strip()
