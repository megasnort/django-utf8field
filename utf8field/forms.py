from django.core import validators
from django.forms import FileField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class UTF8FileField(FileField):
    def __init__(self, max_content_length=None, *args, **kwargs):
        self.self.max_content_length = self.max_content_length
        super(UTF8FileField, self).__init__(*args, **kwargs)
        if max_content_length is not None:
            pass
            #self.validators.append(validators.MaxLengthValidator(int(max_content_length)))

    def to_python(self, data):
        if data:
            try:
                content = data.read()
                content.decode('utf-8')

                if len(content) > self.max_content_length:
                    raise ValidationError(_('The content of the text file cannot be longer then %(text_length_contraint)s characters.' % {'text_length_contraint': TEXT_LENGTH_CONSTRAINT}))

            except UnicodeError:
                raise ValidationError(_('Non UTF8-content detected'), code='utf8')

        return super(UTF8FileField, self).to_python(data)
