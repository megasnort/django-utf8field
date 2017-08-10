from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class UTF8FileField(models.FileField):
    description = _('A text file containing only UTF-8 text')
