from django.conf.urls import include, url
from django.contrib import admin

from dev_example.views import TestCreate, TestMaxContentLengthCreate, TestCreateCharField

urlpatterns = [
    url(r'^char-field/$', TestCreateCharField.as_view(), name='test_view_char_field'),
    url(r'^max-content-length/$', TestMaxContentLengthCreate.as_view(), name='test_max_content_length_view'),
    url(r'^$', TestCreate.as_view(), name='test_view'),
    url(r'^admin/', include(admin.site.urls)),
]
