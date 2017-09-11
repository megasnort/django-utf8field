# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.test import TestCase
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from .models import TestModel, TestCharFieldModel

UTF8_OK_BUT_TOO_LONG_FILE = os.path.join('dev_example', 'tests', 'utf8_ok_but_too_long.txt')
UTF8_OK_FILE = os.path.join('dev_example', 'tests', 'utf8_ok.txt')
UTF8_NOK_FILE = os.path.join('dev_example', 'tests', 'utf8_nok.txt')
UTF8_NOK_ELS_FILE = os.path.join('dev_example', 'tests', 'els_awesome_file.txt')
BINARY_FILE = os.path.join('dev_example', 'tests', 'binky.png')


class CharFieldTests(TestCase):
    def setUp(self):
        self.url = '/char-field/'

    def test_add_view_exists(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input', status_code=200)

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
        with open(UTF8_NOK_FILE, 'rb') as fp:
            response = self.client.post(
                self.url,
                {'text': fp.read(), },
                follow=True
            )
            self.assertEqual(TestCharFieldModel.objects.count(), 0)
            self.assertContains(response, escape(_('Non UTF8-content detected')))

    def test_add_view_shows_error_when_submitting_els_content(self):
        with open(UTF8_NOK_ELS_FILE, 'rb') as fp:
            response = self.client.post(
                self.url,
                {'text': fp.read(), },
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
