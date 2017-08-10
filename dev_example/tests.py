# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.test import TestCase
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from .models import TestModel

UTF8_OK_FILE = os.path.join('dev_example', 'tests', 'utf8_ok.txt')
UTF8_NOK_FILE = os.path.join('dev_example', 'tests', 'utf8_nok.txt')
BINARY_FILE = os.path.join('dev_example', 'tests', 'binky.png')


class ViewTests(TestCase):
    def setUp(self):
        self.url = '/'

    def test_add_view_exists(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<input', status_code=200, count=3)

    def test_add_view_works(self):
        with open(UTF8_OK_FILE) as fp:
            self.client.post(self.url, {'file': fp, })
            self.assertEqual(TestModel.objects.count(), 1)

    def test_when_sending_no_file_when_required_utf8_stuff_should_not_be_triggered(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, escape(_('This field is required.')))
        self.assertEqual(TestModel.objects.count(), 0)

    def test_add_view_shows_error_when_submitting_utf8_file(self):
        with open(UTF8_NOK_FILE) as fp:
            response = self.client.post(
                self.url,
                {'file': fp, },
                follow=True
            )
            self.assertEqual(TestModel.objects.count(), 0)
            self.assertContains(response, escape(_('Non UTF8-content detected')))

    def test_add_view_shows_error_when_submitting_binary_file(self):
        with open(BINARY_FILE ) as fp:
            response = self.client.post(
                self.url,
                {'file': fp, },
                follow=True
            )
            self.assertEqual(TestModel.objects.count(), 0)
            self.assertContains(response, escape(_('Non UTF8-content detected')))
