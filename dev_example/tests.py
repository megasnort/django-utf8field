# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import io
import sys
import json
import ctypes
import unittest

from django.test import TestCase
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from .models import TestModel, TestCharFieldModel, TestTextFieldModel, Message, PermissiveMessage

UTF8_OK_BUT_TOO_LONG_FILE = os.path.join('dev_example', 'tests', 'utf8_ok_but_too_long.txt')
UTF8_OK_FILE = os.path.join('dev_example', 'tests', 'utf8_ok.txt')
UTF8_NOK_FILE = os.path.join('dev_example', 'tests', 'utf8_nok.txt')
UTF8_NOK_ELS_FILE = os.path.join('dev_example', 'tests', 'els_awesome_file.txt')
UTF8_NOK_ORPHEE_FILE = os.path.join('dev_example', 'tests', 'BNC1.txt')
BINARY_FILE = os.path.join('dev_example', 'tests', 'binky.png')


class RestTests(TestCase):
    def setUp(self):
        self.url = '/api/message/'

    def test_add_view_exists(self):
        response = self.client.get(self.url)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_max_content_length(self):
        with open(UTF8_OK_BUT_TOO_LONG_FILE, 'rb') as fp:
            response = self.client.post(
                self.url,
                {'file': fp},
                follow=True
            )

            self.assertEqual(Message.objects.count(), 0)

            if sys.version_info >= (3, 0):
                result = json.loads(response.content.decode('utf-8'))
            else:
                result = json.loads(response.content)

            self.assertTrue(result['file'][0])

            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_add_view_shows_error_when_submitting_4_byte_content_text_field(self):

        with open(UTF8_NOK_ORPHEE_FILE, 'rb') as fp:
            response = self.client.post(
                self.url,
                {
                    'file': fp,
                 },
                follow=True
            )

            result = json.loads(response.content.decode('utf-8'))

            self.assertEqual(result['file'][0], _('4 Byte UTF8-characters detected'))

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Message.objects.count(), 0)

    def test_check_for_null_character_in_char_and_text(self):
        content = ctypes.create_unicode_buffer('String\x00Other')

        response = self.client.post(
            self.url,
            {'text': content, 'char': content, },
            follow=True
        )

        result = json.loads(response.content.decode('utf-8'))

        self.assertEqual(result['text'][0], _('NULL character detected'))
        self.assertEqual(result['char'][0], _('NULL character detected'))
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(TestTextFieldModel.objects.count(), 0)


class TextFieldTests(TestCase):
    def setUp(self):
        self.url = '/text-field/'

    def test_add_view_exists(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input', status_code=200)

    def test_check_for_null_character(self):
        content = ctypes.create_unicode_buffer('String\x00ther')

        response = self.client.post(
            self.url,
            {'text': content, },
            follow=True
        )

        self.assertContains(response, escape(_('NULL character detected')))
        self.assertEqual(TestTextFieldModel.objects.count(), 0)

    def test_add_view_works(self):
        with open(UTF8_OK_FILE, 'rb') as fp:
            response = self.client.post(
                self.url,
                {
                    'text': fp.read()
                },
                follow=True
            )
            self.assertEqual(TestTextFieldModel.objects.count(), 1)
            self.assertEqual(response.status_code, 200)

    def test_check_for_null_character_second_method(self):
        content = 'abcd\x01\x00cdefg'

        response = self.client.post(
            self.url,
            {'text': content, },
            follow=True
        )

        self.assertContains(response, escape(_('NULL character detected')))
        self.assertEqual(TestTextFieldModel.objects.count(), 0)

    def test_add_view_shows_error_when_submitting_els_content(self):
        with open(UTF8_NOK_ELS_FILE, 'rb') as fp:
            response = self.client.post(
                self.url,
                {'text': fp.read(), },
                follow=True
            )

            self.assertContains(response, escape(_('4 Byte UTF8-characters detected')))
            self.assertEqual(TestTextFieldModel.objects.count(), 0)


class CharFieldTests(TestCase):
    def setUp(self):
        self.url = '/char-field/'

    def test_add_view_exists(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input', status_code=200)

    def test_check_for_null_character(self):
        content = ctypes.create_unicode_buffer('String\0Other')

        response = self.client.post(
            self.url,
            {'text': content, },
            follow=True
        )

        self.assertContains(response, escape(_('NULL character detected')))
        self.assertEqual(TestTextFieldModel.objects.count(), 0)

    def test_check_for_null_character_second_method(self):
        content = 'abcd\x01\x00cdefg'

        response = self.client.post(
            self.url,
            {'text': content, },
            follow=True
        )

        self.assertContains(response, escape(_('NULL character detected')))
        self.assertEqual(TestTextFieldModel.objects.count(), 0)

    def test_add_view_works(self):
        with open(UTF8_OK_FILE, 'rb') as fp:
            response = self.client.post(
                self.url,
                {
                    'text': fp.read()
                },
                follow=True
            )

            self.assertEqual(TestCharFieldModel.objects.count(), 1)
            self.assertEqual(response.status_code, 200)


class PermissiveMessageTests(TestCase):
    def setUp(self):
        self.url = '/permissive-message/'

    def tearDown(self):
        for m in PermissiveMessage.objects.all():
            if m.file:
                os.remove(m.file.path)

    def test_view_exists(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input', status_code=200, count=4)

    def test_sending_of_accent_in_char_and_text(self):
        text = 'Gewéldige patiënt!'

        prev_count = PermissiveMessage.objects.count()

        response = self.client.post(
            self.url,
            {'text': text, 'char': text},
            follow=True
        )

        self.assertEqual(PermissiveMessage.objects.count(), prev_count + 1)
        self.assertContains(response, '<input', status_code=200, count=4)

    def test_sending_of_null_character_string_to_char_and_text_should_not_be_possible(self):
        text = '\x00'

        prev_count = PermissiveMessage.objects.count()

        response = self.client.post(
            self.url,
            {'text': text, 'char': text},
            follow=True
        )

        self.assertEqual(PermissiveMessage.objects.count(), prev_count)
        self.assertContains(response, _('NULL character detected'), status_code=200)

    def test_sending_of_4byte_character_string_as_file_should_be_possible(self):
        with open(UTF8_NOK_ELS_FILE, 'rb') as fp:
            text = fp.read()
            fp.seek(0)

            prev_count = PermissiveMessage.objects.count()

            response = self.client.post(
                self.url,
                {'text': text, 'char': text, 'file': fp},
                follow=True
            )
            self.assertEqual(PermissiveMessage.objects.count(), prev_count + 1)
            self.assertNotContains(response, escape(_('4 Byte UTF8-characters detected')), status_code=200)

    def test_sending_of_utf8_characters_should_not_be_possible_in_a_file(self):
        with open(UTF8_NOK_FILE, 'rb') as fp:
            prev_count = PermissiveMessage.objects.count()

            response = self.client.post(
                self.url,
                {'file': fp},
                follow=True
            )
            self.assertEqual(PermissiveMessage.objects.count(), prev_count)
            self.assertContains(response, escape(_('Non UTF8-content detected')), status_code=200)


class FileTests(TestCase):
    def setUp(self):
        self.url = '/'
        self.max_content_length_url = '/max-content-length/'

    def test_add_view_exists(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input', status_code=200, count=3)

    def test_add_view_works(self):
        with open(UTF8_OK_FILE, 'rb') as fp:
            response = self.client.post(self.url, {'file': fp, }, follow=True)
            self.assertEqual(TestModel.objects.count(), 1)
            self.assertEqual(response.status_code, 200)

    def test_when_sending_no_file_when_required_utf8_stuff_should_not_be_triggered(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, escape(_('This field is required.')))
        self.assertEqual(TestModel.objects.count(), 0)

    def test_add_view_shows_error_when_submitting_non_utf8_file(self):
        with open(UTF8_NOK_FILE, 'rb') as fp:
            response = self.client.post(
                self.url,
                {'file': fp, },
                follow=True
            )
            self.assertEqual(TestModel.objects.count(), 0)
            self.assertContains(response, escape(_('Non UTF8-content detected')))

    def test_add_view_shows_error_when_submitting_els_utf8_file(self):
        with open(UTF8_NOK_ELS_FILE, 'rb') as fp:
            response = self.client.post(
                self.url,
                {'file': fp, },
                follow=True
            )
            self.assertEqual(TestModel.objects.count(), 0)
            self.assertContains(response, escape(_('4 Byte UTF8-characters detected')))

    def test_add_view_shows_error_when_submitting_binary_file(self):
        with open(BINARY_FILE, 'rb') as fp:
            response = self.client.post(
                self.url,
                {'file': fp, },
                follow=True
            )
            self.assertEqual(TestModel.objects.count(), 0)
            self.assertContains(response, escape(_('Non UTF8-content detected')))

    def test_max_content_length(self):
        with open(UTF8_OK_BUT_TOO_LONG_FILE, 'rb') as fp:
            response = self.client.post(
                self.max_content_length_url,
                {'file': fp, },
                follow=True
            )

            self.assertEqual(TestModel.objects.count(), 0)
            self.assertContains(
                response,
                escape(
                    _('The content of the text file cannot be longer then %(max_content_length)s characters.' % {
                        'max_content_length': 1000})
                ),
                status_code=200
            )
