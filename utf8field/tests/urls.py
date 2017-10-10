from django.conf.urls import include, url
from django.contrib import admin

from dev_example.views import TestCreate, TestMaxContentLengthCreate, TestCreateCharField, TestCreateTextField,\
    MessageViews, PermissiveMessageCreate

urlpatterns = [
    # rest
    url(r'^api/message/$', MessageViews.as_view(), name='message'),

    # forms
    url(r'^text-field/$', TestCreateTextField.as_view(), name='test_view_text_field'),
    url(r'^char-field/$', TestCreateCharField.as_view(), name='test_view_char_field'),
    url(r'^max-content-length/$', TestMaxContentLengthCreate.as_view(), name='test_max_content_length_view'),
    url(r'^permissive-message/$', PermissiveMessageCreate.as_view(), name='permissive_message_view'),
    url(r'^$', TestCreate.as_view(), name='test_view'),

    # admin, for debugging
    url(r'^admin/', include(admin.site.urls)),
]
