from django.conf.urls import include, url
from django.contrib import admin

from dev_example.views import TestCreate

urlpatterns = [
    url(r'^$', TestCreate.as_view(), name='test_view'),
    url(r'^admin/', include(admin.site.urls)),
]
