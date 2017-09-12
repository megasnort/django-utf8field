# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import io
import sys
import json
import ctypes

from django.test import TestCase
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from .models import TestModel, TestCharFieldModel, TestTextFieldModel

UTF8_OK_BUT_TOO_LONG_FILE = os.path.join('dev_example', 'tests', 'utf8_ok_but_too_long.txt')
UTF8_OK_FILE = os.path.join('dev_example', 'tests', 'utf8_ok.txt')
UTF8_NOK_FILE = os.path.join('dev_example', 'tests', 'utf8_nok.txt')
UTF8_NOK_ELS_FILE = os.path.join('dev_example', 'tests', 'els_awesome_file.txt')
BINARY_FILE = os.path.join('dev_example', 'tests', 'binky.png')


class RestTests(TestCase):
    def setUp(self):
        self.url = '/api/message/'

    def test_add_view_exists(self):
        response = self.client.get(self.url)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_add_view_shows_error_when_submitting_els_content_text_field(self):
        if sys.version_info >= (3, 0):
            with io.open(UTF8_NOK_ELS_FILE, 'r', encoding='utf8') as fp:
                content = fp.read()
                fp.seek(0)
                response = self.client.post(
                    self.url,
                    {
                        'text': content,
                        'char': content,
                        'file': fp

                     },
                    follow=True
                )

                result = json.loads(response.content)
                self.assertEqual(result['text'][0], _('4 Byte UTF8-characters detected'))
                self.assertEqual(result['char'][0], _('4 Byte UTF8-characters detected'))
                self.assertEqual(result['file'][0], _('4 Byte UTF8-characters detected'))
        else:
            with open(UTF8_NOK_ELS_FILE, 'rb') as fp:
                content = str(fp.read())
                fp.seek()
                response = self.client.post(
                    self.url,
                    {
                        'text': content,
                        'char': content,
                        'file': fp,
                     },
                    follow=True
                )

                result = json.loads(response.content.decode('utf-8'))
                self.assertEqual(result['text'][0], _('Non UTF8-content detected'))
                self.assertEqual(result['char'][0], _('Non UTF8-content detected'))
                self.assertEqual(result['file'][0], _('Non UTF8-content detected'))

        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(TestTextFieldModel.objects.count(), 0)

    def test_check_for_null_character(self):
        content = ctypes.create_unicode_buffer('String\0Other')

        response = self.client.post(
            self.url,
            {'text': content, },
            follow=True
        )

        result = json.loads(response.content.decode('utf-8'))

        self.assertEqual(result['text'][0], _('NULL character detected'))
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
        content = ctypes.create_unicode_buffer('String\0Other')

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

    def test_add_view_shows_error_when_submitting_non_utf8_content(self):
        if sys.version_info < (3, 0):
            with open(UTF8_NOK_FILE, 'rb') as fp:
                content = fp.read()
                response = self.client.post(
                    self.url,
                    {'text': str(content), },
                    follow=True
                )
                self.assertEqual(TestTextFieldModel.objects.count(), 0)
                self.assertContains(response, escape(_('Non UTF8-content detected')))

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
        if sys.version_info >= (3, 0):
            with io.open(UTF8_NOK_ELS_FILE, 'r', encoding='utf8') as fp:
                response = self.client.post(
                    self.url,
                    {'text': str(fp.read()), },
                    follow=True
                )
                self.assertContains(response, escape(_('4 Byte UTF8-characters detected')))
                self.assertEqual(TestTextFieldModel.objects.count(), 0)

        else:
            with open(UTF8_NOK_ELS_FILE, 'rb') as fp:
                response = self.client.post(
                    self.url,
                    {'text': str(fp.read()), },
                    follow=True
                )
                self.assertEqual(TestTextFieldModel.objects.count(), 0)
                self.assertContains(response, escape(_('Non UTF8-content detected')))


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

    def test_add_view_shows_error_when_submitting_non_utf8_content(self):
        if sys.version_info < (3, 0):
            with open(UTF8_NOK_FILE, 'rb') as fp:
                content = fp.read()
                response = self.client.post(
                    self.url,
                    {'text': str(content), },
                    follow=True
                )
                self.assertEqual(TestCharFieldModel.objects.count(), 0)
                self.assertContains(response, escape(_('Non UTF8-content detected')))

    def test_add_view_shows_error_when_submitting_els_content(self):
        if sys.version_info >= (3, 0):
            with io.open(UTF8_NOK_ELS_FILE, 'r', encoding='utf8') as fp:
                response = self.client.post(
                    self.url,
                    {'text': str(fp.read()), },
                    follow=True
                )
                self.assertEqual(TestCharFieldModel.objects.count(), 0)
                self.assertContains(response, escape(_('4 Byte UTF8-characters detected')))
        else:
            with open(UTF8_NOK_ELS_FILE, 'rb') as fp:
                response = self.client.post(
                    self.url,
                    {'text': str(fp.read()), },
                    follow=True
                )
                self.assertEqual(TestCharFieldModel.objects.count(), 0)
                self.assertContains(response, escape(_('Non UTF8-content detected')))


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
