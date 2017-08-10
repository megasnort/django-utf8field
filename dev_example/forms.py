from django.forms import ModelForm

from .models import TestModel

class TestForm(ModelForm):

    class Meta:
        model = TestModel
        fields = [
            'file',
        ]


