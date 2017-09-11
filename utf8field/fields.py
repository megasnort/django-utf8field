from __future__ import unicode_literals

import re
import sys

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

re_pattern = re.compile(u'[^\u0000-\u07FF\uE000-\uFFFF]', re.UNICODE)


def filter_using_re(unicode_string):
    return re_pattern.sub(u'\uFFFD', unicode_string)


class UTF8CharField(models.CharField):
    description = _('A char field containing only UTF-8 text')

    def to_python(self, data):
        if data:
            try:
                if sys.version_info >= (3, 0):
                    # in python 3, string are actually unicode
                    decoded = data
                else:
                    decoded = data.decode('utf-8')

                if decoded != filter_using_re(decoded):
                    raise ValidationError(_('4 Byte UTF8-characters detected'), code='utf8')

            except UnicodeError:
                raise ValidationError(_('Non UTF8-content detected'), code='utf8')

        return super(UTF8CharField, self).to_python(data)


class UTF8TextField(models.TextField):
    description = _('A text field containing only UTF-8 text')

    def to_python(self, data):
        if data:
            try:
                if sys.version_info >= (3, 0):
                    # in python 3, string are actually unicode
                    decoded = data
                else:
                    decoded = data.decode('utf-8')

                if decoded != filter_using_re(decoded):
                    raise ValidationError(_('4 Byte UTF8-characters detected'), code='utf8')

            except UnicodeError:
                raise ValidationError(_('Non UTF8-content detected'), code='utf8')

        return super(UTF8TextField, self).to_python(data)


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

    def to_python(self, data):
        if data:
            try:
                content = data.read()
                decoded = content.decode('utf-8')

                if decoded != filter_using_re(decoded):
                    raise ValidationError(_('4 Byte UTF8-characters detected'), code='utf8')

                if self.max_content_length and len(content) > self.max_content_length:
                    raise ValidationError(_(
                        'The content of the text file cannot be longer then %(max_content_length)s characters.' % {
                            'max_content_length': self.max_content_length}))

            except UnicodeError:
                raise ValidationError(_('Non UTF8-content detected'), code='utf8')

        return super(UTF8FileField, self).to_python(data)
