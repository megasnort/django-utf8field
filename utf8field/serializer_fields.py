from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .validators import text_input_validator


class UTF8TextSerializerField(serializers.CharField):
    def to_internal_value(self, data):
        text_input_validator(data, ValidationError)
        return data