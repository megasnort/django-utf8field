from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from utf8field import forms


class UTF8FileField(models.FileField):
    description = _('A text file containing only UTF-8 text')

    def __init__(self, max_content_length=None, *args, **kwargs):
        self.max_content_length = max_content_length
        super(UTF8FileField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(UTF8FileField, self).deconstruct()

        if self.max_content_length:
            kwargs['max_content_length'] = self.max_content_length
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.UTF8FileField}
        defaults.update(kwargs)
        return super(UTF8FileField, self).formfield(**defaults)
